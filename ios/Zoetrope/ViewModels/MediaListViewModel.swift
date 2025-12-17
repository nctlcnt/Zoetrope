import SwiftUI

@MainActor
class MediaListViewModel: ObservableObject {
    @Published var mediaItems: [MediaItem] = []
    @Published var isLoading = false
    @Published var errorMessage: String?
    
    private let apiService = APIService.shared
    
    func loadMediaItems(
        status: MediaStatus? = nil,
        mediaType: MediaType? = nil,
        priority: PriorityLevel? = nil
    ) async {
        isLoading = true
        errorMessage = nil
        
        do {
            mediaItems = try await apiService.fetchMediaItems(
                status: status,
                mediaType: mediaType,
                priority: priority
            )
        } catch {
            errorMessage = "加载失败: \(error.localizedDescription)"
        }
        
        isLoading = false
    }
}
