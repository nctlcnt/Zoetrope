import SwiftUI

struct DashboardView: View {
    @EnvironmentObject var viewModel: DashboardViewModel
    
    var body: some View {
        NavigationView {
            ScrollView {
                VStack(alignment: .leading, spacing: 24) {
                    if let dashboard = viewModel.dashboard {
                        // Latest Wants Carousel
                        CarouselSection(carousel: dashboard.latestWants)
                        
                        // Ending Soon Carousel
                        CarouselSection(carousel: dashboard.endingSoon)
                        
                        // Recently Released Carousel
                        CarouselSection(carousel: dashboard.recentlyReleased)
                    } else if viewModel.isLoading {
                        ProgressView()
                            .frame(maxWidth: .infinity, maxHeight: .infinity)
                    } else if let error = viewModel.errorMessage {
                        VStack {
                            Text(error)
                                .foregroundColor(.red)
                            Button("重试") {
                                Task {
                                    await viewModel.loadDashboard()
                                }
                            }
                        }
                        .frame(maxWidth: .infinity, maxHeight: .infinity)
                    }
                }
                .padding(.vertical)
            }
            .navigationTitle("Zoetrope")
            .refreshable {
                await viewModel.refreshDashboard()
            }
        }
        .task {
            await viewModel.loadDashboard()
        }
    }
}

struct CarouselSection: View {
    let carousel: Carousel
    
    var body: some View {
        VStack(alignment: .leading, spacing: 12) {
            Text(carousel.title)
                .font(.title2)
                .fontWeight(.bold)
                .padding(.horizontal)
            
            if carousel.items.isEmpty {
                Text("暂无内容")
                    .foregroundColor(.secondary)
                    .padding(.horizontal)
            } else {
                ScrollView(.horizontal, showsIndicators: false) {
                    HStack(spacing: 16) {
                        ForEach(carousel.items) { item in
                            NavigationLink(destination: MediaDetailView(mediaId: item.id)) {
                                MediaCardView(item: item)
                            }
                        }
                    }
                    .padding(.horizontal)
                }
            }
        }
    }
}

struct MediaCardView: View {
    let item: MediaItem
    
    var body: some View {
        VStack(alignment: .leading, spacing: 8) {
            // Poster
            AsyncImage(url: item.posterUrl.flatMap(URL.init)) { phase in
                switch phase {
                case .success(let image):
                    image
                        .resizable()
                        .aspectRatio(2/3, contentMode: .fill)
                case .failure(_):
                    placeholderImage
                case .empty:
                    placeholderImage
                @unknown default:
                    placeholderImage
                }
            }
            .frame(width: 150, height: 225)
            .clipShape(RoundedRectangle(cornerRadius: 12))
            .shadow(radius: 4)
            
            // Title
            Text(item.title)
                .font(.headline)
                .lineLimit(2)
                .frame(width: 150, alignment: .leading)
            
            // Rating
            if let rating = item.rating {
                HStack(spacing: 4) {
                    Image(systemName: "star.fill")
                        .foregroundColor(.yellow)
                        .font(.caption)
                    Text(String(format: "%.1f", rating))
                        .font(.caption)
                        .foregroundColor(.secondary)
                }
            }
            
            // Priority badge
            Text(item.priority.displayName)
                .font(.caption2)
                .padding(.horizontal, 8)
                .padding(.vertical, 4)
                .background(Color(hex: item.priority.color).opacity(0.2))
                .foregroundColor(Color(hex: item.priority.color))
                .clipShape(Capsule())
        }
        .frame(width: 150)
    }
    
    private var placeholderImage: some View {
        Rectangle()
            .fill(Color.gray.opacity(0.3))
            .overlay(
                Image(systemName: "film")
                    .font(.largeTitle)
                    .foregroundColor(.gray)
            )
            .frame(width: 150, height: 225)
            .clipShape(RoundedRectangle(cornerRadius: 12))
    }
}

#Preview {
    DashboardView()
        .environmentObject(DashboardViewModel())
}
