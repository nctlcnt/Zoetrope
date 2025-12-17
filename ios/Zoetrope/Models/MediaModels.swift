import Foundation

// MARK: - Enums

enum MediaType: String, Codable, CaseIterable {
    case movie
    case tvShow = "tv_show"
    case novel
    case book
    
    var displayName: String {
        switch self {
        case .movie: return "电影"
        case .tvShow: return "电视剧"
        case .novel: return "小说"
        case .book: return "书籍"
        }
    }
}

enum PriorityLevel: String, Codable, CaseIterable {
    case high
    case medium
    case low
    
    var displayName: String {
        switch self {
        case .high: return "高优先级"
        case .medium: return "中优先级"
        case .low: return "低优先级"
        }
    }
    
    var color: String {
        switch self {
        case .high: return "#FF3B30"
        case .medium: return "#FF9500"
        case .low: return "#34C759"
        }
    }
}

enum MediaStatus: String, Codable {
    case wantToWatch = "want_to_watch"
    case watching
    case watched
    case dropped
    
    var displayName: String {
        switch self {
        case .wantToWatch: return "想看"
        case .watching: return "在看"
        case .watched: return "看过"
        case .dropped: return "弃剧"
        }
    }
}

// MARK: - Models

struct MediaItem: Identifiable, Codable {
    let id: Int
    let title: String
    let mediaType: MediaType
    let status: MediaStatus
    let priority: PriorityLevel
    let reasonToWatch: String?
    let trailerUrl: String?
    let recommendationText: String?
    let releaseDate: Date?
    let endDate: Date?
    let posterUrl: String?
    let rating: Double?
    let aiSummary: String?
    let aiMotivation: String?
    let appearanceCount: Int
    let createdAt: Date
    let updatedAt: Date
    let recommendations: [Recommendation]
    let streamingLinks: [StreamingLink]
    
    enum CodingKeys: String, CodingKey {
        case id, title, status, priority, rating
        case mediaType = "media_type"
        case reasonToWatch = "reason_to_watch"
        case trailerUrl = "trailer_url"
        case recommendationText = "recommendation_text"
        case releaseDate = "release_date"
        case endDate = "end_date"
        case posterUrl = "poster_url"
        case aiSummary = "ai_summary"
        case aiMotivation = "ai_motivation"
        case appearanceCount = "appearance_count"
        case createdAt = "created_at"
        case updatedAt = "updated_at"
        case recommendations
        case streamingLinks = "streaming_links"
    }
}

struct Recommendation: Identifiable, Codable {
    let id: Int
    let sourceName: String
    let sourceUrl: String?
    let recommendationReason: String?
    let rating: Double?
    let reviewDate: Date?
    let createdAt: Date
    
    enum CodingKeys: String, CodingKey {
        case id, rating
        case sourceName = "source_name"
        case sourceUrl = "source_url"
        case recommendationReason = "recommendation_reason"
        case reviewDate = "review_date"
        case createdAt = "created_at"
    }
}

struct StreamingLink: Identifiable, Codable {
    let id: Int
    let platform: String
    let url: String
    let available: Bool
    let createdAt: Date
    
    enum CodingKeys: String, CodingKey {
        case id, platform, url, available
        case createdAt = "created_at"
    }
}

struct Carousel: Identifiable, Codable {
    var id: String { title }
    let title: String
    let items: [MediaItem]
}

struct Dashboard: Codable {
    let latestWants: Carousel
    let endingSoon: Carousel
    let recentlyReleased: Carousel
    
    enum CodingKeys: String, CodingKey {
        case latestWants = "latest_wants"
        case endingSoon = "ending_soon"
        case recentlyReleased = "recently_released"
    }
}

// MARK: - Request Models

struct MediaItemCreate: Codable {
    let title: String
    let mediaType: MediaType
    let reasonToWatch: String?
    let trailerUrl: String?
    let recommendationText: String?
    let priority: PriorityLevel
    
    enum CodingKeys: String, CodingKey {
        case title, priority
        case mediaType = "media_type"
        case reasonToWatch = "reason_to_watch"
        case trailerUrl = "trailer_url"
        case recommendationText = "recommendation_text"
    }
}
