import SwiftUI

struct MediaDetailView: View {
    let mediaId: Int
    @State private var mediaItem: MediaItem?
    @State private var isLoading = true
    @State private var errorMessage: String?
    @State private var showDeleteConfirmation = false
    @Environment(\.dismiss) private var dismiss
    
    var body: some View {
        ScrollView {
            if let item = mediaItem {
                VStack(alignment: .leading, spacing: 20) {
                    // Header with poster and basic info
                    HStack(alignment: .top, spacing: 16) {
                        AsyncImage(url: item.posterUrl.flatMap(URL.init)) { phase in
                            switch phase {
                            case .success(let image):
                                image.resizable().aspectRatio(contentMode: .fill)
                            case .failure(_), .empty:
                                Rectangle()
                                    .fill(Color.gray.opacity(0.3))
                                    .overlay(Image(systemName: "film").foregroundColor(.gray))
                            @unknown default:
                                Rectangle().fill(Color.gray.opacity(0.3))
                            }
                        }
                        .frame(width: 120, height: 180)
                        .clipShape(RoundedRectangle(cornerRadius: 12))
                        .shadow(radius: 4)
                        
                        VStack(alignment: .leading, spacing: 8) {
                            Text(item.mediaType.displayName)
                                .font(.caption)
                                .foregroundColor(.secondary)
                            
                            if let rating = item.rating {
                                HStack(spacing: 4) {
                                    Image(systemName: "star.fill")
                                        .foregroundColor(.yellow)
                                    Text(String(format: "%.1f", rating))
                                        .font(.headline)
                                }
                            }
                            
                            Text(item.priority.displayName)
                                .font(.caption)
                                .padding(.horizontal, 8)
                                .padding(.vertical, 4)
                                .background(Color(hex: item.priority.color).opacity(0.2))
                                .foregroundColor(Color(hex: item.priority.color))
                                .clipShape(Capsule())
                            
                            if let releaseDate = item.releaseDate {
                                Label(formatDate(releaseDate), systemImage: "calendar")
                                    .font(.caption)
                                    .foregroundColor(.secondary)
                            }
                        }
                    }
                    .padding()
                    
                    // AI Summary
                    if let summary = item.aiSummary {
                        VStack(alignment: .leading, spacing: 8) {
                            Text("AI 分析")
                                .font(.headline)
                            Text(summary)
                                .font(.body)
                                .foregroundColor(.secondary)
                        }
                        .padding()
                        .background(Color.blue.opacity(0.1))
                        .clipShape(RoundedRectangle(cornerRadius: 12))
                        .padding(.horizontal)
                    }
                    
                    // Viewing Motivation
                    if let motivation = item.aiMotivation {
                        VStack(alignment: .leading, spacing: 8) {
                            Text("观看动机")
                                .font(.headline)
                            Text(motivation)
                                .font(.body)
                                .foregroundColor(.secondary)
                        }
                        .padding()
                        .background(Color.green.opacity(0.1))
                        .clipShape(RoundedRectangle(cornerRadius: 12))
                        .padding(.horizontal)
                    }
                    
                    // User's reason
                    if let reason = item.reasonToWatch {
                        VStack(alignment: .leading, spacing: 8) {
                            Text("想看的原因")
                                .font(.headline)
                            Text(reason)
                                .font(.body)
                        }
                        .padding()
                        .background(Color.gray.opacity(0.1))
                        .clipShape(RoundedRectangle(cornerRadius: 12))
                        .padding(.horizontal)
                    }
                    
                    // Recommendations
                    if !item.recommendations.isEmpty {
                        VStack(alignment: .leading, spacing: 12) {
                            Text("推荐来源")
                                .font(.headline)
                                .padding(.horizontal)
                            
                            ForEach(item.recommendations) { rec in
                                RecommendationCard(recommendation: rec)
                                    .padding(.horizontal)
                            }
                        }
                    }
                    
                    // Streaming Links
                    if !item.streamingLinks.isEmpty {
                        VStack(alignment: .leading, spacing: 12) {
                            Text("观看平台")
                                .font(.headline)
                                .padding(.horizontal)
                            
                            ForEach(item.streamingLinks) { link in
                                Button(action: {
                                    APIService.shared.openStreamingPlatform(link)
                                }) {
                                    HStack {
                                        Image(systemName: "play.circle.fill")
                                        Text(link.platform)
                                        Spacer()
                                        Image(systemName: "arrow.up.right")
                                    }
                                    .padding()
                                    .background(Color.red.opacity(0.1))
                                    .clipShape(RoundedRectangle(cornerRadius: 12))
                                }
                                .buttonStyle(PlainButtonStyle())
                                .padding(.horizontal)
                            }
                        }
                    }
                    
                    // Trailer Link
                    if let trailerUrl = item.trailerUrl, let url = URL(string: trailerUrl) {
                        Button(action: {
                            #if os(iOS)
                            UIApplication.shared.open(url)
                            #endif
                        }) {
                            HStack {
                                Image(systemName: "play.rectangle.fill")
                                Text("观看预告片")
                                Spacer()
                                Image(systemName: "arrow.up.right")
                            }
                            .padding()
                            .background(Color.orange.opacity(0.2))
                            .clipShape(RoundedRectangle(cornerRadius: 12))
                        }
                        .buttonStyle(PlainButtonStyle())
                        .padding(.horizontal)
                    }
                    
                    // Delete button
                    Button(role: .destructive, action: {
                        showDeleteConfirmation = true
                    }) {
                        Text("删除")
                            .frame(maxWidth: .infinity)
                            .padding()
                            .background(Color.red.opacity(0.1))
                            .foregroundColor(.red)
                            .clipShape(RoundedRectangle(cornerRadius: 12))
                    }
                    .padding()
                }
            } else if isLoading {
                ProgressView()
                    .frame(maxWidth: .infinity, maxHeight: .infinity)
            } else if let error = errorMessage {
                Text(error)
                    .foregroundColor(.red)
            }
        }
        .navigationTitle(mediaItem?.title ?? "")
        .navigationBarTitleDisplayMode(.inline)
        .task {
            await loadMediaItem()
        }
        .confirmationDialog("确定删除这个项目吗？", isPresented: $showDeleteConfirmation) {
            Button("删除", role: .destructive) {
                Task {
                    await deleteMedia()
                }
            }
        }
    }
    
    private func loadMediaItem() async {
        isLoading = true
        errorMessage = nil
        
        do {
            mediaItem = try await APIService.shared.fetchMediaItem(id: mediaId)
        } catch {
            errorMessage = "加载失败: \(error.localizedDescription)"
        }
        
        isLoading = false
    }
    
    private func deleteMedia() async {
        do {
            try await APIService.shared.deleteMediaItem(id: mediaId)
            await MainActor.run {
                dismiss()
            }
        } catch {
            errorMessage = "删除失败: \(error.localizedDescription)"
        }
    }
    
    private func formatDate(_ date: Date) -> String {
        let formatter = DateFormatter()
        formatter.dateStyle = .medium
        return formatter.string(from: date)
    }
}

struct RecommendationCard: View {
    let recommendation: Recommendation
    
    var body: some View {
        VStack(alignment: .leading, spacing: 8) {
            HStack {
                Text(recommendation.sourceName)
                    .font(.subheadline)
                    .fontWeight(.semibold)
                
                if let rating = recommendation.rating {
                    Spacer()
                    HStack(spacing: 4) {
                        Image(systemName: "star.fill")
                            .foregroundColor(.yellow)
                            .font(.caption)
                        Text(String(format: "%.1f", rating))
                            .font(.caption)
                    }
                }
            }
            
            if let reason = recommendation.recommendationReason {
                Text(reason)
                    .font(.caption)
                    .foregroundColor(.secondary)
            }
        }
        .padding()
        .background(Color.gray.opacity(0.1))
        .clipShape(RoundedRectangle(cornerRadius: 12))
    }
}

#Preview {
    NavigationView {
        MediaDetailView(mediaId: 1)
    }
}
