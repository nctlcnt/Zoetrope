import SwiftUI

struct MediaListView: View {
    @StateObject private var viewModel = MediaListViewModel()
    @State private var selectedStatus: MediaStatus? = .wantToWatch
    @State private var selectedType: MediaType? = nil
    @State private var selectedPriority: PriorityLevel? = nil
    
    var body: some View {
        NavigationView {
            VStack {
                // Filters
                ScrollView(.horizontal, showsIndicators: false) {
                    HStack(spacing: 12) {
                        FilterChip(
                            title: "全部状态",
                            isSelected: selectedStatus == nil
                        ) {
                            selectedStatus = nil
                        }
                        
                        ForEach(MediaStatus.allCases, id: \.self) { status in
                            FilterChip(
                                title: status.displayName,
                                isSelected: selectedStatus == status
                            ) {
                                selectedStatus = status
                            }
                        }
                    }
                    .padding(.horizontal)
                }
                .padding(.vertical, 8)
                
                // List
                List {
                    ForEach(viewModel.mediaItems) { item in
                        NavigationLink(destination: MediaDetailView(mediaId: item.id)) {
                            MediaRowView(item: item)
                        }
                    }
                }
                .listStyle(.plain)
            }
            .navigationTitle("我的收藏")
            .onChange(of: selectedStatus) { _ in
                Task {
                    await viewModel.loadMediaItems(
                        status: selectedStatus,
                        mediaType: selectedType,
                        priority: selectedPriority
                    )
                }
            }
        }
        .task {
            await viewModel.loadMediaItems(status: .wantToWatch)
        }
    }
}

struct MediaRowView: View {
    let item: MediaItem
    
    var body: some View {
        HStack(spacing: 12) {
            // Poster
            AsyncImage(url: item.posterUrl.flatMap(URL.init)) { phase in
                switch phase {
                case .success(let image):
                    image
                        .resizable()
                        .aspectRatio(contentMode: .fill)
                case .failure(_), .empty:
                    Rectangle()
                        .fill(Color.gray.opacity(0.3))
                        .overlay(Image(systemName: "film").foregroundColor(.gray))
                @unknown default:
                    Rectangle().fill(Color.gray.opacity(0.3))
                }
            }
            .frame(width: 60, height: 90)
            .clipShape(RoundedRectangle(cornerRadius: 8))
            
            // Info
            VStack(alignment: .leading, spacing: 4) {
                Text(item.title)
                    .font(.headline)
                    .lineLimit(2)
                
                Text(item.mediaType.displayName)
                    .font(.caption)
                    .foregroundColor(.secondary)
                
                if let rating = item.rating {
                    HStack(spacing: 4) {
                        Image(systemName: "star.fill")
                            .foregroundColor(.yellow)
                            .font(.caption2)
                        Text(String(format: "%.1f", rating))
                            .font(.caption)
                            .foregroundColor(.secondary)
                    }
                }
                
                Text(item.priority.displayName)
                    .font(.caption2)
                    .padding(.horizontal, 6)
                    .padding(.vertical, 2)
                    .background(Color(hex: item.priority.color).opacity(0.2))
                    .foregroundColor(Color(hex: item.priority.color))
                    .clipShape(Capsule())
            }
            
            Spacer()
        }
        .padding(.vertical, 4)
    }
}

struct FilterChip: View {
    let title: String
    let isSelected: Bool
    let action: () -> Void
    
    var body: some View {
        Button(action: action) {
            Text(title)
                .font(.subheadline)
                .padding(.horizontal, 12)
                .padding(.vertical, 6)
                .background(isSelected ? Color.red : Color.gray.opacity(0.2))
                .foregroundColor(isSelected ? .white : .primary)
                .clipShape(Capsule())
        }
    }
}

extension MediaStatus: CaseIterable {
    static var allCases: [MediaStatus] {
        [.wantToWatch, .watching, .watched, .dropped]
    }
}

#Preview {
    MediaListView()
}
