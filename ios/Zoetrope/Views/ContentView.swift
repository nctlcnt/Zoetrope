import SwiftUI

struct ContentView: View {
    @EnvironmentObject var viewModel: DashboardViewModel
    @State private var selectedTab = 0
    
    var body: some View {
        TabView(selection: $selectedTab) {
            DashboardView()
                .tabItem {
                    Label("首页", systemImage: "house.fill")
                }
                .tag(0)
            
            MediaListView()
                .tabItem {
                    Label("列表", systemImage: "list.bullet")
                }
                .tag(1)
            
            AddMediaView()
                .tabItem {
                    Label("添加", systemImage: "plus.circle.fill")
                }
                .tag(2)
        }
        .accentColor(.red)
    }
}

#Preview {
    ContentView()
        .environmentObject(DashboardViewModel())
}
