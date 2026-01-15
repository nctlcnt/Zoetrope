//
//  APIManager.swift
//  Zoetrope
//
//  API 管理器
//  统一管理所有外部 API 的调用
//  包括 TMDB、AI 服务、自建后端等
//

import Foundation

// MARK: - API 错误类型
/// 定义 API 调用可能出现的错误
enum APIError: Error, LocalizedError {
    case invalidURL              // URL 无效
    case networkError(Error)     // 网络错误
    case decodingError(Error)    // 解码错误
    case serverError(Int)        // 服务器错误（HTTP 状态码）
    case unauthorized            // 未授权（API Key 无效）
    case rateLimited             // 请求频率超限
    case noData                  // 无数据返回

    /// 错误描述
    var errorDescription: String? {
        switch self {
        case .invalidURL:
            return "无效的 URL"
        case .networkError(let error):
            return "网络错误: \(error.localizedDescription)"
        case .decodingError(let error):
            return "数据解析错误: \(error.localizedDescription)"
        case .serverError(let code):
            return "服务器错误: \(code)"
        case .unauthorized:
            return "API 密钥无效或已过期"
        case .rateLimited:
            return "请求频率超限，请稍后重试"
        case .noData:
            return "服务器未返回数据"
        }
    }
}

// MARK: - API 服务类型
/// 定义支持的 API 服务类型
enum APIServiceType {
    case tmdb       // TMDB 电影数据库
    case openAI     // OpenAI API
    case claude     // Claude API
    case backend    // 自建后端

    /// 获取对应的 Base URL
    var baseURL: String {
        switch self {
        case .tmdb:
            return "https://api.themoviedb.org/3"
        case .openAI:
            return "https://api.openai.com/v1"
        case .claude:
            return "https://api.anthropic.com/v1"
        case .backend:
            // 本地开发环境使用 localhost
            // TODO: 生产环境替换为实际的后端地址
            return "http://localhost:8000/api"
        }
    }
}

// MARK: - HTTP 请求方法
/// 定义支持的 HTTP 方法
enum HTTPMethod: String {
    case GET = "GET"
    case POST = "POST"
    case PUT = "PUT"
    case DELETE = "DELETE"
    case PATCH = "PATCH"
}

// MARK: - API 管理器
/// 统一的 API 管理器
/// 负责处理所有外部 API 请求
/// 使用单例模式确保全局只有一个实例
class APIManager {
    // MARK: 单例
    /// 共享实例
    static let shared = APIManager()

    // MARK: 私有属性
    /// URL Session 用于网络请求
    private let session: URLSession

    /// JSON 解码器
    private let decoder: JSONDecoder

    /// JSON 编码器
    private let encoder: JSONEncoder

    // MARK: 初始化
    /// 私有初始化方法，确保单例模式
    private init() {
        // 配置 URLSession
        let config = URLSessionConfiguration.default
        config.timeoutIntervalForRequest = 30  // 请求超时 30 秒
        config.timeoutIntervalForResource = 60 // 资源超时 60 秒
        self.session = URLSession(configuration: config)

        // 配置 JSON 解码器
        self.decoder = JSONDecoder()
        self.decoder.keyDecodingStrategy = .convertFromSnakeCase
        self.decoder.dateDecodingStrategy = .iso8601

        // 配置 JSON 编码器
        self.encoder = JSONEncoder()
        self.encoder.keyEncodingStrategy = .convertToSnakeCase
    }

    // MARK: - 通用请求方法

    /// 发起 API 请求
    /// - Parameters:
    ///   - service: API 服务类型
    ///   - endpoint: 接口路径（如 "/search/movie"）
    ///   - method: HTTP 方法
    ///   - parameters: 查询参数（用于 GET 请求）
    ///   - body: 请求体（用于 POST/PUT 请求）
    ///   - headers: 额外的请求头
    /// - Returns: 解码后的响应数据
    func request<T: Decodable>(
        service: APIServiceType,
        endpoint: String,
        method: HTTPMethod = .GET,
        parameters: [String: String]? = nil,
        body: Encodable? = nil,
        headers: [String: String]? = nil
    ) async throws -> T {
        // 1. 构建 URL
        var urlString = service.baseURL + endpoint

        // 添加查询参数（用于 GET 请求）
        if let parameters = parameters, !parameters.isEmpty {
            let queryString = parameters
                .map { "\($0.key)=\($0.value.addingPercentEncoding(withAllowedCharacters: .urlQueryAllowed) ?? $0.value)" }
                .joined(separator: "&")
            urlString += "?\(queryString)"
        }

        guard let url = URL(string: urlString) else {
            throw APIError.invalidURL
        }

        // 2. 构建请求
        var request = URLRequest(url: url)
        request.httpMethod = method.rawValue

        // 3. 添加通用请求头
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        request.setValue("application/json", forHTTPHeaderField: "Accept")

        // 4. 添加 API 认证头
        addAuthorizationHeader(to: &request, for: service)

        // 5. 添加额外的请求头
        headers?.forEach { key, value in
            request.setValue(value, forHTTPHeaderField: key)
        }

        // 6. 添加请求体（用于 POST/PUT 请求）
        if let body = body {
            request.httpBody = try encoder.encode(AnyEncodable(body))
        }

        // 7. 发起请求
        let (data, response) = try await session.data(for: request)

        // 8. 检查响应状态
        guard let httpResponse = response as? HTTPURLResponse else {
            throw APIError.noData
        }

        // 9. 处理 HTTP 状态码
        switch httpResponse.statusCode {
        case 200...299:
            // 成功
            break
        case 401:
            throw APIError.unauthorized
        case 429:
            throw APIError.rateLimited
        default:
            throw APIError.serverError(httpResponse.statusCode)
        }

        // 10. 解码响应数据
        do {
            return try decoder.decode(T.self, from: data)
        } catch {
            throw APIError.decodingError(error)
        }
    }

    // MARK: - 认证头处理

    /// 为请求添加认证头
    /// - Parameters:
    ///   - request: URL 请求（inout）
    ///   - service: API 服务类型
    private func addAuthorizationHeader(to request: inout URLRequest, for service: APIServiceType) {
        switch service {
        case .tmdb:
            // TMDB 使用 Bearer Token
            if let apiKey = SecretManager.shared.getAPIKey(for: .tmdb) {
                request.setValue("Bearer \(apiKey)", forHTTPHeaderField: "Authorization")
            }

        case .openAI:
            // OpenAI 使用 Bearer Token
            if let apiKey = SecretManager.shared.getAPIKey(for: .openAI) {
                request.setValue("Bearer \(apiKey)", forHTTPHeaderField: "Authorization")
            }

        case .claude:
            // Claude 使用 x-api-key 头
            if let apiKey = SecretManager.shared.getAPIKey(for: .claude) {
                request.setValue(apiKey, forHTTPHeaderField: "x-api-key")
                request.setValue("2023-06-01", forHTTPHeaderField: "anthropic-version")
            }

        case .backend:
            // 自建后端的认证方式（待实现）
            // TODO: 实现后端认证逻辑
            break
        }
    }
}

// MARK: - TMDB API 扩展
extension APIManager {
    /// 搜索电影
    /// - Parameter query: 搜索关键词
    /// - Returns: 搜索结果
    func searchMovies(query: String) async throws -> TMDBSearchResponse {
        return try await request(
            service: .tmdb,
            endpoint: "/search/movie",
            parameters: [
                "query": query,
                "language": "zh-CN",
                "include_adult": "false"
            ]
        )
    }

    /// 搜索电视剧
    /// - Parameter query: 搜索关键词
    /// - Returns: 搜索结果
    func searchTVShows(query: String) async throws -> TMDBSearchResponse {
        return try await request(
            service: .tmdb,
            endpoint: "/search/tv",
            parameters: [
                "query": query,
                "language": "zh-CN"
            ]
        )
    }

    /// 获取电影详情
    /// - Parameter id: 电影 ID
    /// - Returns: 电影详情
    func getMovieDetails(id: Int) async throws -> TMDBMovieDetails {
        return try await request(
            service: .tmdb,
            endpoint: "/movie/\(id)",
            parameters: ["language": "zh-CN"]
        )
    }
}

// MARK: - AI API 扩展
extension APIManager {
    /// 使用 AI 分析文本内容
    /// - Parameter content: 待分析的文本
    /// - Returns: 分析结果
    func analyzeContent(_ content: String) async throws -> AIAnalysisResult {
        // TODO: 实现 AI 分析逻辑
        // 可以根据配置选择 OpenAI 或 Claude
        fatalError("AI 分析功能待实现")
    }
}

// MARK: - 辅助类型

/// 搜索范围枚举
enum SearchScope: String {
    case tmdb = "tmdb"              // TMDB 综合搜索
    case tmdbMovie = "tmdb_movie"   // TMDB 电影搜索
    case tmdbTV = "tmdb_tv"         // TMDB 电视剧搜索
    case media = "media"            // 本地媒体库搜索
}

/// 类型擦除的 Encodable 包装器
/// 用于处理泛型 Encodable 参数
private struct AnyEncodable: Encodable {
    private let encode: (Encoder) throws -> Void

    init<T: Encodable>(_ value: T) {
        self.encode = value.encode(to:)
    }

    func encode(to encoder: Encoder) throws {
        try encode(encoder)
    }
}

// MARK: - TMDB 响应模型（临时定义，后续移到单独文件）

/// TMDB 搜索响应
struct TMDBSearchResponse: Decodable {
    let page: Int
    let results: [TMDBMediaItem]
    let totalPages: Int
    let totalResults: Int
}

/// TMDB 媒体条目
struct TMDBMediaItem: Decodable {
    let id: Int
    let title: String?       // 电影标题
    let name: String?        // 电视剧名称
    let overview: String?
    let posterPath: String?
    let releaseDate: String? // 电影上映日期
    let firstAirDate: String? // 电视剧首播日期

    /// 获取显示标题（电影或电视剧）
    var displayTitle: String {
        return title ?? name ?? "未知"
    }
}

/// TMDB 电影详情
struct TMDBMovieDetails: Decodable {
    let id: Int
    let title: String
    let overview: String?
    let posterPath: String?
    let releaseDate: String?
    let runtime: Int?
    let genres: [TMDBGenre]?
}

/// TMDB 类型
struct TMDBGenre: Decodable {
    let id: Int
    let name: String
}

/// AI 分析结果
struct AIAnalysisResult: Decodable {
    let title: String
    let summary: String
    let sentiment: Double
    let mediaType: String
}

// MARK: - Backend API 扩展
extension APIManager {
    /// 统一搜索接口
    /// - Parameters:
    ///   - query: 搜索关键词
    ///   - scope: 搜索范围 (tmdb/tmdb_movie/tmdb_tv/media)
    ///   - page: 页码
    ///   - year: 年份过滤（可选）
    /// - Returns: 搜索结果
    func search(
        query: String,
        scope: SearchScope = .tmdb,
        page: Int = 1,
        year: Int? = nil
    ) async throws -> TMDBSearchResponse {
        var params: [String: String] = [
            "query": query,
            "scope": scope.rawValue,
            "page": String(page)
        ]
        if let year = year {
            params["year"] = String(year)
        }
        return try await request(
            service: .backend,
            endpoint: "/search",
            parameters: params
        )
    }

    /// 提交内容到收集箱
    /// - Parameters:
    ///   - content: 用户粘贴的文本内容
    ///   - url: 可选的原始 URL
    /// - Returns: 收集箱条目响应
    func submitToInbox(content: String, url: String? = nil) async throws -> InboxItemResponse {
        let requestBody = InboxSubmitRequest(content: content, url: url)
        return try await request(
            service: .backend,
            endpoint: "/inbox/submit",
            method: .POST,
            body: requestBody
        )
    }

    /// 搜索媒体（通过后端代理 TMDB）
    /// - Parameters:
    ///   - query: 搜索关键词
    ///   - type: 媒体类型 (movie/tv/multi)
    /// - Returns: 搜索结果
    func searchMedia(query: String, type: String = "multi") async throws -> TMDBSearchResponse {
        return try await request(
            service: .backend,
            endpoint: "/tmdb/search/\(type)",
            parameters: ["query": query]
        )
    }

    /// 添加媒体到收藏
    /// - Parameter item: TMDB 搜索结果中的媒体项
    /// - Returns: 添加后的媒体响应
    func addMedia(from item: TMDBMediaItem) async throws -> MediaAddResponse {
        let requestBody = MediaAddRequest(
            tmdbId: item.id,
            title: item.displayTitle,
            mediaType: item.title != nil ? "movie" : "tv",
            overview: item.overview,
            posterPath: item.posterPath,
            releaseDate: item.releaseDate ?? item.firstAirDate
        )
        return try await request(
            service: .backend,
            endpoint: "/media/add",
            method: .POST,
            body: requestBody
        )
    }
}

// MARK: - Backend 请求/响应模型

/// 收集箱提交请求
struct InboxSubmitRequest: Encodable {
    let content: String
    let url: String?
}

/// 收集箱条目响应
struct InboxItemResponse: Decodable {
    let id: Int
    let rawContent: String
    let url: String?
    let processed: Bool
    let processingError: String?
    let extractedTitles: [String]?
    let createdAt: String
    let expiresAt: String
}

/// 添加媒体请求
struct MediaAddRequest: Encodable {
    let tmdbId: Int
    let title: String
    let mediaType: String
    let overview: String?
    let posterPath: String?
    let releaseDate: String?
}

/// 添加媒体响应
struct MediaAddResponse: Decodable {
    let id: Int
    let title: String
    let type: String
    let tmdbId: Int?
    let releaseDate: String?
    let posterUrl: String?
    let overview: String?
    let userScore: Double?
    let priorityScore: Double
    let mentionCount: Int
    let isWatched: Int
    let isHidden: Bool
    let createdAt: String
    let updatedAt: String
}
