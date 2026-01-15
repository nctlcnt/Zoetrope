//
//  MediaItem.swift
//  Zoetrope
//
//  媒体条目数据模型
//  用于表示电影、电视剧、小说等媒体内容
//

import Foundation

// MARK: - 媒体类型枚举
/// 定义支持的媒体类型
/// MVP阶段仅支持电影和电视剧，后续可扩展
enum MediaType: String, CaseIterable, Identifiable {
    case movie = "movie"        // 电影
    case tvShow = "tv"          // 电视剧
    case novel = "novel"        // 小说（后续扩展）
    case book = "book"          // 书籍（后续扩展）
    case music = "music"        // 音乐（后续扩展）

    var id: String { rawValue }

    /// 返回媒体类型的显示名称
    var displayName: String {
        switch self {
        case .movie: return "电影"
        case .tvShow: return "电视剧"
        case .novel: return "小说"
        case .book: return "书籍"
        case .music: return "音乐"
        }
    }

    /// 返回对应的SF Symbol图标名称
    var iconName: String {
        switch self {
        case .movie: return "film"
        case .tvShow: return "tv"
        case .novel: return "book.closed"
        case .book: return "books.vertical"
        case .music: return "music.note"
        }
    }
}

// MARK: - 媒体条目模型
/// 媒体条目的核心数据结构
/// 包含媒体的基本信息、评分、优先级等
struct MediaItem: Identifiable {
    // MARK: 基本属性

    /// 唯一标识符
    let id: UUID

    /// 媒体标题
    let title: String

    /// 媒体类型（电影/电视剧/小说等）
    let type: MediaType

    /// 上映/发布日期
    let releaseDate: Date?

    /// 下映日期（仅对电影有效）
    /// 用于计算"即将下映"提醒
    let endDate: Date?

    /// 海报图片URL
    /// 用于在列表和详情页展示
    let posterURL: String?

    /// 简介/预览文本
    /// 用于在列表中显示的简短描述
    /// 可以是AI生成的摘要或用户添加的备注
    var summary: String?

    // MARK: 评分相关

    /// 用户手动评分 (0-10)
    /// nil表示用户尚未评分
    var userScore: Double?

    /// 系统计算的优先级评分
    /// 基于时间因素、热度、用户兴趣等多维度计算
    /// 用于决定在轮播区的展示顺序
    var priorityScore: Double

    /// 被提到的次数
    /// 出现在多个榜单/博文中会增加此计数
    /// 是热度计算的重要因素
    var mentionCount: Int

    // MARK: 时间戳

    /// 创建时间
    let createdAt: Date

    /// 最后更新时间
    var updatedAt: Date

    // MARK: 状态标记

    /// 是否已观看/阅读
    var isWatched: Bool

    /// 用户是否标记为"不感兴趣"
    /// 影响优先级排序
    var isNotInterested: Bool

    // MARK: 初始化方法

    /// 创建新的媒体条目
    /// - Parameters:
    ///   - title: 媒体标题
    ///   - type: 媒体类型
    ///   - releaseDate: 上映/发布日期（可选）
    ///   - posterURL: 海报图片URL（可选）
    ///   - summary: 简介/预览文本（可选）
    init(
        title: String,
        type: MediaType,
        releaseDate: Date? = nil,
        endDate: Date? = nil,
        posterURL: String? = nil,
        summary: String? = nil
    ) {
        self.id = UUID()
        self.title = title
        self.type = type
        self.releaseDate = releaseDate
        self.endDate = endDate
        self.posterURL = posterURL
        self.summary = summary
        self.userScore = nil
        self.priorityScore = 0.0
        self.mentionCount = 1
        self.createdAt = Date()
        self.updatedAt = Date()
        self.isWatched = false
        self.isNotInterested = false
    }
}

// MARK: - 计算属性扩展
extension MediaItem {
    /// 检查是否即将上映（7天内）
    var isComingSoon: Bool {
        guard let releaseDate = releaseDate else { return false }
        let daysUntilRelease = Calendar.current.dateComponents(
            [.day],
            from: Date(),
            to: releaseDate
        ).day ?? 0
        return daysUntilRelease > 0 && daysUntilRelease <= 7
    }

    /// 检查是否即将下映（7天内）
    /// 用于触发"即将下映"提醒
    var isEndingSoon: Bool {
        guard let endDate = endDate else { return false }
        let daysUntilEnd = Calendar.current.dateComponents(
            [.day],
            from: Date(),
            to: endDate
        ).day ?? 0
        return daysUntilEnd > 0 && daysUntilEnd <= 7
    }

    /// 检查是否正在上映/已发布
    var isNowShowing: Bool {
        guard let releaseDate = releaseDate else { return false }
        let now = Date()
        // 如果有下映日期，检查是否在上映期间
        if let endDate = endDate {
            return now >= releaseDate && now <= endDate
        }
        // 没有下映日期，只检查是否已发布
        return now >= releaseDate
    }

    /// 格式化的上映日期字符串
    var releaseDateString: String? {
        guard let releaseDate = releaseDate else { return nil }
        let formatter = DateFormatter()
        formatter.dateFormat = "yyyy年M月d日"
        return formatter.string(from: releaseDate)
    }
}

// MARK: - 示例数据（用于预览和测试）
extension MediaItem {
    /// 生成示例数据，用于UI预览和开发测试
    static var sampleItems: [MediaItem] {
        [
            MediaItem(
                title: "沙丘3",
                type: .movie,
                releaseDate: Calendar.current.date(byAdding: .day, value: 3, to: Date()),
                posterURL: nil,
                summary: "保罗·厄崔迪的史诗旅程继续，他必须在爱情与宇宙命运之间做出抉择。维伦纽瓦执导的科幻巨制第三部。"
            ),
            MediaItem(
                title: "三体",
                type: .tvShow,
                releaseDate: Calendar.current.date(byAdding: .day, value: -10, to: Date()),
                posterURL: nil,
                summary: "根据刘慈欣同名小说改编，讲述地球文明与三体文明的首次接触。Netflix出品，口碑爆棚。"
            ),
            MediaItem(
                title: "奥本海默",
                type: .movie,
                releaseDate: Calendar.current.date(byAdding: .month, value: -2, to: Date()),
                endDate: Calendar.current.date(byAdding: .day, value: 5, to: Date()),
                posterURL: nil,
                summary: "诺兰执导，基里安·墨菲主演。讲述原子弹之父奥本海默的传奇一生，获奥斯卡最佳影片。"
            ),
            MediaItem(
                title: "繁花",
                type: .tvShow,
                releaseDate: Calendar.current.date(byAdding: .day, value: -30, to: Date()),
                posterURL: nil,
                summary: "王家卫执导首部电视剧，胡歌主演。讲述90年代上海的商战传奇，画面精美绝伦。"
            ),
            MediaItem(
                title: "热辣滚烫",
                type: .movie,
                releaseDate: Calendar.current.date(byAdding: .day, value: -5, to: Date()),
                posterURL: nil,
                summary: "贾玲自导自演，讲述一个普通女孩通过拳击改变人生的励志故事。春节档票房冠军。"
            )
        ]
    }
}
