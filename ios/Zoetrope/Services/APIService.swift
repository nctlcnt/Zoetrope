import Foundation

class APIService: ObservableObject {
    static let shared = APIService()
    
    // Change this to your backend URL
    private let baseURL = "http://localhost:8000"
    
    private let decoder: JSONDecoder = {
        let decoder = JSONDecoder()
        decoder.dateDecodingStrategy = .iso8601
        return decoder
    }()
    
    private let encoder: JSONEncoder = {
        let encoder = JSONEncoder()
        encoder.dateEncodingStrategy = .iso8601
        return encoder
    }()
    
    // MARK: - Dashboard
    
    func fetchDashboard() async throws -> Dashboard {
        let url = URL(string: "\(baseURL)/dashboard")!
        let (data, _) = try await URLSession.shared.data(from: url)
        return try decoder.decode(Dashboard.self, from: data)
    }
    
    // MARK: - Media Items
    
    func fetchMediaItems(
        status: MediaStatus? = nil,
        mediaType: MediaType? = nil,
        priority: PriorityLevel? = nil
    ) async throws -> [MediaItem] {
        var components = URLComponents(string: "\(baseURL)/media")!
        var queryItems: [URLQueryItem] = []
        
        if let status = status {
            queryItems.append(URLQueryItem(name: "status", value: status.rawValue))
        }
        if let mediaType = mediaType {
            queryItems.append(URLQueryItem(name: "media_type", value: mediaType.rawValue))
        }
        if let priority = priority {
            queryItems.append(URLQueryItem(name: "priority", value: priority.rawValue))
        }
        
        if !queryItems.isEmpty {
            components.queryItems = queryItems
        }
        
        let (data, _) = try await URLSession.shared.data(from: components.url!)
        return try decoder.decode([MediaItem].self, from: data)
    }
    
    func fetchMediaItem(id: Int) async throws -> MediaItem {
        let url = URL(string: "\(baseURL)/media/\(id)")!
        let (data, _) = try await URLSession.shared.data(from: url)
        return try decoder.decode(MediaItem.self, from: data)
    }
    
    func createMediaItem(_ item: MediaItemCreate) async throws -> MediaItem {
        let url = URL(string: "\(baseURL)/media")!
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        request.httpBody = try encoder.encode(item)
        
        let (data, response) = try await URLSession.shared.data(for: request)
        
        guard let httpResponse = response as? HTTPURLResponse,
              (200...299).contains(httpResponse.statusCode) else {
            throw APIError.invalidResponse
        }
        
        return try decoder.decode(MediaItem.self, from: data)
    }
    
    func deleteMediaItem(id: Int) async throws {
        let url = URL(string: "\(baseURL)/media/\(id)")!
        var request = URLRequest(url: url)
        request.httpMethod = "DELETE"
        
        let (_, response) = try await URLSession.shared.data(for: request)
        
        guard let httpResponse = response as? HTTPURLResponse,
              (200...299).contains(httpResponse.statusCode) else {
            throw APIError.invalidResponse
        }
    }
    
    // MARK: - Platform Links
    
    func openStreamingPlatform(_ link: StreamingLink) {
        if let url = URL(string: link.url) {
            #if os(iOS)
            UIApplication.shared.open(url)
            #endif
        }
    }
}

enum APIError: Error {
    case invalidResponse
    case decodingError
}
