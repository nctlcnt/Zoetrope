import SwiftUI

@main
struct ZoetropeApp: App {
    @StateObject private var viewModel = DashboardViewModel()
    
    var body: some Scene {
        WindowGroup {
            ContentView()
                .environmentObject(viewModel)
        }
    }
}
