//
//  SecretManager.swift
//  Zoetrope
//
//  密钥管理器
//  安全地存储和管理 API 密钥等敏感信息
//  使用 Keychain 进行安全存储
//

import Foundation
import Security

// MARK: - API 密钥类型
/// 定义支持的 API 密钥类型
enum APIKeyType: String, CaseIterable {
    case tmdb = "tmdb_api_key"           // TMDB API 密钥
    case openAI = "openai_api_key"       // OpenAI API 密钥
    case claude = "claude_api_key"       // Claude API 密钥
    case backend = "backend_api_key"     // 自建后端 API 密钥

    /// 密钥的显示名称
    var displayName: String {
        switch self {
        case .tmdb: return "TMDB"
        case .openAI: return "OpenAI"
        case .claude: return "Claude"
        case .backend: return "后端服务"
        }
    }

    /// 密钥的说明
    var description: String {
        switch self {
        case .tmdb:
            return "用于获取电影/电视剧信息，从 themoviedb.org 获取"
        case .openAI:
            return "用于 AI 文本分析，从 platform.openai.com 获取"
        case .claude:
            return "用于 AI 文本分析，从 console.anthropic.com 获取"
        case .backend:
            return "用于连接 Zoetrope 后端服务"
        }
    }
}

// MARK: - Keychain 错误类型
/// Keychain 操作可能出现的错误
enum KeychainError: Error, LocalizedError {
    case duplicateItem          // 密钥已存在
    case itemNotFound           // 密钥不存在
    case unexpectedStatus(OSStatus) // 其他错误

    var errorDescription: String? {
        switch self {
        case .duplicateItem:
            return "密钥已存在"
        case .itemNotFound:
            return "密钥不存在"
        case .unexpectedStatus(let status):
            return "Keychain 错误: \(status)"
        }
    }
}

// MARK: - 密钥管理器
/// 密钥管理器
/// 使用 Keychain 安全存储 API 密钥
/// 单例模式确保全局只有一个实例
class SecretManager {
    // MARK: 单例
    /// 共享实例
    static let shared = SecretManager()

    // MARK: 私有属性
    /// Keychain 服务标识符
    /// 用于区分不同应用的密钥
    private let serviceName = "com.zoetrope.app"

    /// 内存缓存
    /// 避免频繁读取 Keychain
    private var cache: [APIKeyType: String] = [:]

    // MARK: 初始化
    /// 私有初始化方法，确保单例模式
    private init() {
        // 预加载所有密钥到缓存
        preloadKeys()
    }

    // MARK: - 公开方法

    /// 获取 API 密钥
    /// - Parameter type: 密钥类型
    /// - Returns: 密钥值，如果不存在则返回 nil
    func getAPIKey(for type: APIKeyType) -> String? {
        // 先从缓存获取
        if let cachedKey = cache[type] {
            return cachedKey
        }

        // 从 Keychain 读取
        if let key = readFromKeychain(key: type.rawValue) {
            cache[type] = key
            return key
        }

        return nil
    }

    /// 保存 API 密钥
    /// - Parameters:
    ///   - key: 密钥值
    ///   - type: 密钥类型
    /// - Throws: KeychainError
    func saveAPIKey(_ key: String, for type: APIKeyType) throws {
        // 先尝试删除旧密钥（如果存在）
        try? deleteAPIKey(for: type)

        // 保存到 Keychain
        try saveToKeychain(key: type.rawValue, value: key)

        // 更新缓存
        cache[type] = key
    }

    /// 删除 API 密钥
    /// - Parameter type: 密钥类型
    /// - Throws: KeychainError
    func deleteAPIKey(for type: APIKeyType) throws {
        try deleteFromKeychain(key: type.rawValue)

        // 从缓存移除
        cache.removeValue(forKey: type)
    }

    /// 检查密钥是否存在
    /// - Parameter type: 密钥类型
    /// - Returns: 是否存在
    func hasAPIKey(for type: APIKeyType) -> Bool {
        return getAPIKey(for: type) != nil
    }

    /// 获取所有已配置的密钥类型
    /// - Returns: 已配置密钥的类型列表
    func getConfiguredKeyTypes() -> [APIKeyType] {
        return APIKeyType.allCases.filter { hasAPIKey(for: $0) }
    }

    /// 清除所有密钥
    /// - Throws: KeychainError
    func clearAllKeys() throws {
        for type in APIKeyType.allCases {
            try? deleteAPIKey(for: type)
        }
        cache.removeAll()
    }

    // MARK: - 私有方法

    /// 预加载所有密钥到缓存
    private func preloadKeys() {
        for type in APIKeyType.allCases {
            if let key = readFromKeychain(key: type.rawValue) {
                cache[type] = key
            }
        }
    }

    /// 从 Keychain 读取数据
    /// - Parameter key: 键名
    /// - Returns: 值，如果不存在则返回 nil
    private func readFromKeychain(key: String) -> String? {
        // 构建查询条件
        let query: [String: Any] = [
            kSecClass as String: kSecClassGenericPassword,
            kSecAttrService as String: serviceName,
            kSecAttrAccount as String: key,
            kSecReturnData as String: true,
            kSecMatchLimit as String: kSecMatchLimitOne
        ]

        // 执行查询
        var result: AnyObject?
        let status = SecItemCopyMatching(query as CFDictionary, &result)

        // 检查结果
        guard status == errSecSuccess,
              let data = result as? Data,
              let value = String(data: data, encoding: .utf8) else {
            return nil
        }

        return value
    }

    /// 保存数据到 Keychain
    /// - Parameters:
    ///   - key: 键名
    ///   - value: 值
    /// - Throws: KeychainError
    private func saveToKeychain(key: String, value: String) throws {
        guard let data = value.data(using: .utf8) else {
            throw KeychainError.unexpectedStatus(errSecParam)
        }

        // 构建保存条目
        let query: [String: Any] = [
            kSecClass as String: kSecClassGenericPassword,
            kSecAttrService as String: serviceName,
            kSecAttrAccount as String: key,
            kSecValueData as String: data,
            kSecAttrAccessible as String: kSecAttrAccessibleWhenUnlockedThisDeviceOnly
        ]

        // 执行保存
        let status = SecItemAdd(query as CFDictionary, nil)

        // 检查结果
        switch status {
        case errSecSuccess:
            return
        case errSecDuplicateItem:
            throw KeychainError.duplicateItem
        default:
            throw KeychainError.unexpectedStatus(status)
        }
    }

    /// 从 Keychain 删除数据
    /// - Parameter key: 键名
    /// - Throws: KeychainError
    private func deleteFromKeychain(key: String) throws {
        // 构建删除条件
        let query: [String: Any] = [
            kSecClass as String: kSecClassGenericPassword,
            kSecAttrService as String: serviceName,
            kSecAttrAccount as String: key
        ]

        // 执行删除
        let status = SecItemDelete(query as CFDictionary)

        // 检查结果
        switch status {
        case errSecSuccess, errSecItemNotFound:
            return
        default:
            throw KeychainError.unexpectedStatus(status)
        }
    }
}

// MARK: - 开发环境支持
#if DEBUG
extension SecretManager {
    /// 从环境变量加载密钥（仅开发环境）
    /// 用于开发时快速配置，避免手动输入
    func loadFromEnvironment() {
        // 从环境变量读取密钥
        if let tmdbKey = ProcessInfo.processInfo.environment["TMDB_API_KEY"] {
            try? saveAPIKey(tmdbKey, for: .tmdb)
        }

        if let openAIKey = ProcessInfo.processInfo.environment["OPENAI_API_KEY"] {
            try? saveAPIKey(openAIKey, for: .openAI)
        }

        if let claudeKey = ProcessInfo.processInfo.environment["CLAUDE_API_KEY"] {
            try? saveAPIKey(claudeKey, for: .claude)
        }
    }

    /// 打印当前密钥配置状态（仅开发环境）
    func printStatus() {
        print("=== SecretManager Status ===")
        for type in APIKeyType.allCases {
            let status = hasAPIKey(for: type) ? "✓ 已配置" : "✗ 未配置"
            print("\(type.displayName): \(status)")
        }
        print("============================")
    }
}
#endif

// MARK: - 使用示例（注释）
/*

 // 保存密钥
 try SecretManager.shared.saveAPIKey("your-api-key", for: .tmdb)

 // 获取密钥
 if let apiKey = SecretManager.shared.getAPIKey(for: .tmdb) {
     print("TMDB API Key: \(apiKey)")
 }

 // 检查密钥是否存在
 if SecretManager.shared.hasAPIKey(for: .openAI) {
     // 使用 OpenAI API
 }

 // 删除密钥
 try SecretManager.shared.deleteAPIKey(for: .claude)

 // 开发环境：从环境变量加载
 #if DEBUG
 SecretManager.shared.loadFromEnvironment()
 SecretManager.shared.printStatus()
 #endif

 */
