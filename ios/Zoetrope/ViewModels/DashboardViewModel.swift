import SwiftUI

@MainActor
class DashboardViewModel: ObservableObject {
    @Published var dashboard: Dashboard?
    @Published var isLoading = false
    @Published var errorMessage: String?
    
    private let apiService = APIService.shared
    
    func loadDashboard() async {
        isLoading = true
        errorMessage = nil
        
        do {
            dashboard = try await apiService.fetchDashboard()
        } catch {
            errorMessage = "加载失败: \(error.localizedDescription)"
        }
        
        isLoading = false
    }
    
    func refreshDashboard() async {
        await loadDashboard()
    }
}
