//
//  MediaListView.swift
//  Zoetrope
//
//  媒体列表组件
//  用于在主界面下半部分展示用户收藏的媒体列表
//  支持多种排序方式
//

import SwiftUI

// MARK: - 排序方式枚举
/// 定义媒体列表的排序方式
/// 用户可以切换不同的排序逻辑来浏览内容
enum SortOption: String, CaseIterable, Identifiable {
    case recentlyAdded = "recently_added"     // 最近添加
    case recentlyUpdated = "recently_updated" // 最近更新
    case commentCount = "comment_count"       // 评论数
    case userScore = "user_score"             // 用户评分
    case popularity = "popularity"            // 热度（被提到次数）

    var id: String { rawValue }

    /// 排序方式的显示名称
    var displayName: String {
        switch self {
        case .recentlyAdded: return "最近添加"
        case .recentlyUpdated: return "最近更新"
        case .commentCount: return "评论数"
        case .userScore: return "评分"
        case .popularity: return "热度"
        }
    }

    /// 排序方式对应的图标
    var iconName: String {
        switch self {
        case .recentlyAdded: return "plus.circle"
        case .recentlyUpdated: return "clock.arrow.circlepath"
        case .commentCount: return "text.bubble"
        case .userScore: return "star"
        case .popularity: return "flame"
        }
    }
}

// MARK: - 媒体列表主视图
/// 媒体列表视图组件
/// 展示用户收藏的所有媒体条目
/// 提供排序切换和筛选功能
struct MediaListView: View {
    // MARK: 属性

    /// 要展示的媒体条目列表
    let items: [MediaItem]

    /// 当前选中的排序方式
    @State private var selectedSort: SortOption = .recentlyAdded

    /// 当前选中的媒体类型筛选（nil表示显示全部）
    @State private var selectedType: MediaType? = nil

    /// 点击条目进入详情的回调
    var onItemTapped: ((MediaItem) -> Void)?

    // MARK: 视图主体
    var body: some View {
        VStack(spacing: 0) {
            // ========================================
            // 顶部工具栏：排序和筛选
            // ========================================
            ListToolbarView(
                selectedSort: $selectedSort,
                selectedType: $selectedType
            )

            // ========================================
            // 分隔线
            // ========================================
            Divider()

            // ========================================
            // 媒体列表内容
            // 使用ScrollView + LazyVStack实现高性能列表
            // LazyVStack会延迟加载，优化内存使用
            // ========================================
            ScrollView {
                LazyVStack(spacing: 0) {
                    // 根据筛选和排序后的数据渲染列表
                    ForEach(filteredAndSortedItems) { item in
                        // 单个列表行
                        MediaListRowView(item: item)
                            .onTapGesture {
                                // 点击进入详情页
                                onItemTapped?(item)
                            }

                        // 行间分隔线
                        Divider()
                            .padding(.leading, 80) // 左侧留出缩略图宽度的间距
                    }
                }
            }
        }
    }

    // MARK: 计算属性

    /// 根据当前筛选和排序条件处理后的数据
    private var filteredAndSortedItems: [MediaItem] {
        var result = items

        // 第一步：按类型筛选
        if let type = selectedType {
            result = result.filter { $0.type == type }
        }

        // 第二步：按选中的方式排序
        // 注意：这里只是演示排序逻辑，实际排序应该在ViewModel中处理
        switch selectedSort {
        case .recentlyAdded:
            // 按添加时间倒序（最新的在前）
            result.sort { $0.createdAt > $1.createdAt }
        case .recentlyUpdated:
            // 按更新时间倒序
            result.sort { $0.updatedAt > $1.updatedAt }
        case .commentCount:
            // 按提及次数倒序（暂时用mentionCount代替评论数）
            result.sort { $0.mentionCount > $1.mentionCount }
        case .userScore:
            // 按用户评分倒序，未评分的排在后面
            result.sort { ($0.userScore ?? 0) > ($1.userScore ?? 0) }
        case .popularity:
            // 按热度（被提到次数）倒序
            result.sort { $0.mentionCount > $1.mentionCount }
        }

        return result
    }
}

// MARK: - 列表工具栏
/// 列表顶部的工具栏
/// 包含排序选择和类型筛选
struct ListToolbarView: View {
    /// 绑定：当前选中的排序方式
    @Binding var selectedSort: SortOption

    /// 绑定：当前选中的类型筛选
    @Binding var selectedType: MediaType?

    var body: some View {
        HStack {
            // ========================================
            // 排序选择菜单
            // 使用Menu组件实现下拉选择
            // ========================================
            Menu {
                // 遍历所有排序选项
                ForEach(SortOption.allCases) { option in
                    Button(action: {
                        selectedSort = option
                    }) {
                        HStack {
                            Image(systemName: option.iconName)
                            Text(option.displayName)
                            // 当前选中的选项显示勾号
                            if selectedSort == option {
                                Spacer()
                                Image(systemName: "checkmark")
                            }
                        }
                    }
                }
            } label: {
                // 菜单按钮样式
                HStack(spacing: 4) {
                    Image(systemName: selectedSort.iconName)
                    Text(selectedSort.displayName)
                    Image(systemName: "chevron.down")
                        .font(.caption)
                }
                .font(.subheadline)
                .foregroundColor(.primary)
                .padding(.horizontal, 12)
                .padding(.vertical, 8)
                .background(Color.gray.opacity(0.1))
                .cornerRadius(8)
            }

            Spacer()

            // ========================================
            // 类型筛选标签
            // 水平滚动的标签栏
            // ========================================
            ScrollView(.horizontal, showsIndicators: false) {
                HStack(spacing: 8) {
                    // "全部"选项
                    FilterChipView(
                        title: "全部",
                        isSelected: selectedType == nil,
                        action: { selectedType = nil }
                    )

                    // MVP阶段仅显示电影和电视剧
                    FilterChipView(
                        title: MediaType.movie.displayName,
                        icon: MediaType.movie.iconName,
                        isSelected: selectedType == .movie,
                        action: { selectedType = .movie }
                    )

                    FilterChipView(
                        title: MediaType.tvShow.displayName,
                        icon: MediaType.tvShow.iconName,
                        isSelected: selectedType == .tvShow,
                        action: { selectedType = .tvShow }
                    )
                }
            }
        }
        .padding(.horizontal, 16)
        .padding(.vertical, 12)
        // 使用跨平台兼容的背景色
        #if os(macOS)
        .background(Color(nsColor: .windowBackgroundColor))
        #else
        .background(Color(uiColor: .systemBackground))
        #endif
    }
}

// MARK: - 筛选标签组件
/// 单个筛选标签（Chip）
/// 用于类型筛选的可点击标签
struct FilterChipView: View {
    /// 标签文字
    let title: String

    /// 可选的图标名称
    var icon: String? = nil

    /// 是否选中
    let isSelected: Bool

    /// 点击回调
    let action: () -> Void

    var body: some View {
        Button(action: action) {
            HStack(spacing: 4) {
                // 显示图标（如果有）
                if let iconName = icon {
                    Image(systemName: iconName)
                        .font(.caption)
                }
                Text(title)
                    .font(.subheadline)
            }
            .padding(.horizontal, 12)
            .padding(.vertical, 6)
            // 选中状态使用不同的背景色
            .background(isSelected ? Color.blue : Color.gray.opacity(0.1))
            .foregroundColor(isSelected ? .white : .primary)
            .cornerRadius(16)
        }
    }
}

// MARK: - 媒体列表行视图
/// 单个媒体条目在列表中的展示样式
/// 布局：左侧海报 + 右侧（标题 + 预览文字 + 底部信息）
struct MediaListRowView: View {
    /// 要展示的媒体条目
    let item: MediaItem

    var body: some View {
        HStack(alignment: .top, spacing: 12) {
            // ========================================
            // 左侧：海报缩略图
            // 固定尺寸，使用渐变色作为占位背景
            // 实际项目中会使用 AsyncImage 加载真实海报
            // ========================================
            ZStack {
                // 海报背景（渐变色占位）
                RoundedRectangle(cornerRadius: 8)
                    .fill(
                        LinearGradient(
                            colors: posterGradient(for: item.type),
                            startPoint: .topLeading,
                            endPoint: .bottomTrailing
                        )
                    )

                // 媒体类型图标（当没有海报时显示）
                Image(systemName: item.type.iconName)
                    .font(.title)
                    .foregroundColor(.white.opacity(0.8))
            }
            .frame(width: 70, height: 100)
            // 添加轻微阴影增加层次感
            .shadow(color: .black.opacity(0.1), radius: 2, x: 0, y: 1)

            // ========================================
            // 右侧：标题 + 预览 + 底部信息
            // ========================================
            VStack(alignment: .leading, spacing: 6) {
                // ----------------------------------
                // 标题行：标题 + 可选的状态标签
                // ----------------------------------
                HStack(alignment: .top) {
                    Text(item.title)
                        .font(.headline)
                        .fontWeight(.semibold)
                        .lineLimit(1)

                    Spacer()

                    // 右上角显示评分（如果有）
                    if let score = item.userScore {
                        HStack(spacing: 2) {
                            Image(systemName: "star.fill")
                                .font(.caption2)
                                .foregroundColor(.yellow)
                            Text(String(format: "%.1f", score))
                                .font(.caption)
                                .fontWeight(.medium)
                        }
                        .padding(.horizontal, 6)
                        .padding(.vertical, 2)
                        .background(Color.yellow.opacity(0.15))
                        .cornerRadius(4)
                    }
                }

                // ----------------------------------
                // 预览文字：显示简介内容
                // 最多显示2-3行，超出部分省略
                // ----------------------------------
                if let summary = item.summary, !summary.isEmpty {
                    Text(summary)
                        .font(.subheadline)
                        .foregroundColor(.secondary)
                        .lineLimit(2)
                        .lineSpacing(2)
                }

                Spacer(minLength: 4)

                // ----------------------------------
                // 底部信息行：类型、日期、状态标签
                // ----------------------------------
                HStack(spacing: 8) {
                    // 媒体类型
                    Label(item.type.displayName, systemImage: item.type.iconName)
                        .font(.caption)
                        .foregroundColor(.secondary)

                    // 分隔点
                    if item.releaseDateString != nil {
                        Text("·")
                            .foregroundColor(.secondary)
                    }

                    // 上映日期
                    if let dateString = item.releaseDateString {
                        Text(dateString)
                            .font(.caption)
                            .foregroundColor(.secondary)
                    }

                    Spacer()

                    // 状态标签（优先显示一个最重要的）
                    if item.isEndingSoon {
                        StatusBadge(text: "即将下映", color: .red)
                    } else if item.isComingSoon {
                        StatusBadge(text: "即将上映", color: .green)
                    } else if item.isNowShowing {
                        StatusBadge(text: "热映中", color: .orange)
                    } else if item.isWatched {
                        StatusBadge(text: "已看", color: .gray)
                    }
                }
            }
            // 让右侧内容占据剩余空间
            .frame(maxWidth: .infinity, alignment: .leading)
        }
        .padding(.horizontal, 16)
        .padding(.vertical, 12)
        // 确保整行都可点击
        .contentShape(Rectangle())
    }

    // MARK: 辅助方法

    /// 根据媒体类型返回海报渐变色
    /// - Parameter type: 媒体类型
    /// - Returns: 渐变色数组
    private func posterGradient(for type: MediaType) -> [Color] {
        switch type {
        case .movie:
            return [Color.blue, Color.indigo]
        case .tvShow:
            return [Color.orange, Color.red]
        case .novel:
            return [Color.green, Color.teal]
        case .book:
            return [Color.brown, Color.orange]
        case .music:
            return [Color.pink, Color.purple]
        }
    }
}

// MARK: - 预览
#Preview("媒体列表") {
    MediaListView(items: MediaItem.sampleItems)
}

#Preview("列表行", traits:.sizeThatFitsLayout) {
    MediaListRowView(item: MediaItem.sampleItems[0])
}

#Preview("工具栏", traits: .sizeThatFitsLayout) {
    ListToolbarView(
        selectedSort: .constant(.recentlyAdded),
        selectedType: .constant(nil)
    )
}
