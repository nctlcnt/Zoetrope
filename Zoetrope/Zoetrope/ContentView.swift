//
//  ContentView.swift
//  Zoetrope
//
//  主界面视图
//  作为APP的默认界面，整合轮播区和列表区
//
//  Created by A ChaCha on 2026/1/2.
//

import SwiftUI

// MARK: - 主界面视图
/// APP的主界面
/// 布局结构：
/// - 顶部：导航栏（标题 + 添加按钮）
/// - 上半部分：轮播区（CarouselView）
/// - 下半部分：媒体列表（MediaListView）
struct ContentView: View {
    // MARK: 状态属性

    /// 媒体条目数据
    /// 实际项目中应该从ViewModel或数据存储获取
    /// 这里使用示例数据进行演示
    @State private var mediaItems: [MediaItem] = MediaItem.sampleItems

    /// 控制添加内容面板的显示
    @State private var showAddSheet: Bool = false

    /// 当前选中的媒体条目（用于展示详情）
    @State private var selectedItem: MediaItem? = nil

    // MARK: 视图主体
    var body: some View {
        NavigationStack {
            // ========================================
            // 主内容区域
            // 使用ScrollView包裹整体内容，支持滚动
            // ========================================
            ScrollView {
                VStack(spacing: 0) {
                    // ========================================
                    // 上半部分：轮播推荐区
                    // 展示最近上映、高热度、即将下映等推荐内容
                    // ========================================
                    CarouselView(
                        // 筛选出需要在轮播区展示的高优先级条目
                        // 实际项目中应该根据优先级评分排序
                        items: carouselItems,
                        // 用户点击"不感兴趣"的回调
                        onNotInterested: { item in
                            handleNotInterested(item)
                        },
                        // 用户点击"稍后再看"的回调
                        onWatchLater: { item in
                            handleWatchLater(item)
                        },
                        // 用户点击条目进入详情的回调
                        onItemTapped: { item in
                            selectedItem = item
                        }
                    )

                    // ========================================
                    // 分隔区域
                    // 在轮播区和列表区之间添加视觉分隔
                    // ========================================
                    SectionHeaderView(title: "我的收藏")

                    // ========================================
                    // 下半部分：媒体列表区
                    // 展示用户收藏的所有媒体条目
                    // 支持多种排序和筛选方式
                    // ========================================
                    MediaListView(
                        items: mediaItems,
                        onItemTapped: { item in
                            selectedItem = item
                        }
                    )
                    // 设置列表的最小高度，确保界面美观
                    .frame(minHeight: 400)
                }
            }
            // 禁用ScrollView的弹性效果，提供更原生的体验
            .scrollBounceBehavior(.basedOnSize)
            // ========================================
            // 导航栏配置
            // ========================================
            .navigationTitle("Zoetrope")
            .navigationBarTitleDisplayMode(.large)
            .toolbar {
                // 右上角：添加按钮
                ToolbarItem(placement: .navigationBarTrailing) {
                    Button(action: {
                        showAddSheet = true
                    }) {
                        Image(systemName: "plus.circle.fill")
                            .font(.title2)
                    }
                }
            }
            // ========================================
            // 添加内容面板（Sheet）
            // 点击添加按钮时弹出
            // ========================================
            .sheet(isPresented: $showAddSheet) {
                AddContentView(onDismiss: {
                    showAddSheet = false
                })
            }
            // ========================================
            // 详情页导航
            // 点击媒体条目时展示详情
            // ========================================
            .sheet(item: $selectedItem) { item in
                MediaDetailView(item: item)
            }
        }
    }

    // MARK: 计算属性

    /// 轮播区展示的条目
    /// 根据以下条件筛选和排序：
    /// 1. 即将上映的内容
    /// 2. 即将下映的内容（高优先级）
    /// 3. 热映中的内容
    /// 4. 高热度内容
    private var carouselItems: [MediaItem] {
        // 筛选条件：未标记为"不感兴趣"
        let filtered = mediaItems.filter { !$0.isNotInterested }

        // 按优先级排序（这里简化处理，实际应该使用优先级评分）
        // 排序逻辑：即将下映 > 即将上映 > 热映中 > 其他
        return filtered.sorted { item1, item2 in
            // 即将下映的优先级最高
            if item1.isEndingSoon && !item2.isEndingSoon { return true }
            if !item1.isEndingSoon && item2.isEndingSoon { return false }

            // 其次是即将上映
            if item1.isComingSoon && !item2.isComingSoon { return true }
            if !item1.isComingSoon && item2.isComingSoon { return false }

            // 然后是热映中
            if item1.isNowShowing && !item2.isNowShowing { return true }
            if !item1.isNowShowing && item2.isNowShowing { return false }

            // 最后按热度排序
            return item1.mentionCount > item2.mentionCount
        }
    }

    // MARK: 交互处理方法

    /// 处理用户点击"不感兴趣"
    /// - Parameter item: 被标记的媒体条目
    private func handleNotInterested(_ item: MediaItem) {
        // 找到对应的条目并更新状态
        if let index = mediaItems.firstIndex(where: { $0.id == item.id }) {
            mediaItems[index].isNotInterested = true
            // 实际项目中这里应该：
            // 1. 更新本地数据存储
            // 2. 同步到后端
            // 3. 重新计算优先级评分
        }
    }

    /// 处理用户点击"稍后再看"
    /// - Parameter item: 被标记的媒体条目
    private func handleWatchLater(_ item: MediaItem) {
        // 找到对应的条目并调整排序
        if let index = mediaItems.firstIndex(where: { $0.id == item.id }) {
            // 降低优先级评分
            mediaItems[index].priorityScore -= 10
            // 更新时间戳
            mediaItems[index].updatedAt = Date()
            // 实际项目中这里应该触发重新排序
        }
    }
}

// MARK: - 区块标题组件
/// 用于分隔不同区块的标题栏
struct SectionHeaderView: View {
    /// 区块标题文字
    let title: String

    var body: some View {
        HStack {
            Text(title)
                .font(.headline)
                .foregroundColor(.primary)
            Spacer()
        }
        .padding(.horizontal, 16)
        .padding(.vertical, 12)
        .background(Color.secondary.opacity(0.1))
    }
}

// MARK: - 添加内容视图（占位）
/// 添加内容的面板视图
/// MVP阶段仅提供文字输入功能
/// 后续可扩展URL输入、粘贴博文等功能
struct AddContentView: View {
    /// 用户输入的文本内容
    @State private var inputText: String = ""

    /// 加载状态
    @State private var isLoading: Bool = false

    /// 添加中的项目 ID（用于显示加载状态）
    @State private var addingItemId: Int? = nil

    /// 已添加的项目 ID 集合
    @State private var addedItemIds: Set<Int> = []

    /// 错误信息
    @State private var errorMessage: String? = nil

    /// 搜索结果
    @State private var searchResults: [TMDBMediaItem] = []

    /// 是否显示搜索结果
    @State private var showResults: Bool = false

    /// 关闭面板的回调
    var onDismiss: (() -> Void)?

    var body: some View {
        NavigationStack {
            VStack(spacing: 20) {
                // ========================================
                // 说明文字
                // ========================================
                Text("搜索想看的内容")
                    .font(.headline)
                    .padding(.top, 20)

                Text("输入电影或电视剧名称进行搜索")
                    .font(.subheadline)
                    .foregroundColor(.secondary)
                    .multilineTextAlignment(.center)
                    .padding(.horizontal, 20)

                // ========================================
                // 输入区域
                // ========================================
                HStack {
                    TextField("输入名称...", text: $inputText)
                        .textFieldStyle(.plain)
                        .disabled(isLoading)
                        .onSubmit {
                            Task {
                                await searchContent()
                            }
                        }

                    if isLoading {
                        ProgressView()
                            .scaleEffect(0.8)
                    }
                }
                .padding(12)
                .background(Color.gray.opacity(0.1))
                .cornerRadius(10)
                .padding(.horizontal, 16)

                // ========================================
                // 错误提示
                // ========================================
                if let error = errorMessage {
                    Text(error)
                        .font(.caption)
                        .foregroundColor(.red)
                        .padding(.horizontal, 16)
                }

                // ========================================
                // 搜索按钮
                // ========================================
                Button(action: {
                    Task {
                        await searchContent()
                    }
                }) {
                    HStack {
                        Image(systemName: "magnifyingglass")
                        Text(isLoading ? "搜索中..." : "搜索")
                            .font(.headline)
                    }
                    .foregroundColor(.white)
                    .frame(maxWidth: .infinity)
                    .padding()
                    .background(inputText.isEmpty || isLoading ? Color.gray : Color.blue)
                    .cornerRadius(12)
                }
                .disabled(inputText.isEmpty || isLoading)
                .padding(.horizontal, 16)

                // ========================================
                // 搜索结果列表
                // ========================================
                if showResults {
                    if searchResults.isEmpty {
                        Text("未找到相关内容")
                            .foregroundColor(.secondary)
                            .padding(.top, 20)
                    } else {
                        List(searchResults, id: \.id) { item in
                            SearchResultRow(
                                item: item,
                                isAdding: addingItemId == item.id,
                                isAdded: addedItemIds.contains(item.id)
                            ) {
                                Task {
                                    await addMedia(item)
                                }
                            }
                        }
                        .listStyle(.plain)
                    }
                }

                Spacer()
            }
            .navigationTitle("添加内容")
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                // 关闭按钮
                ToolbarItem(placement: .navigationBarLeading) {
                    Button("取消") {
                        onDismiss?()
                    }
                    .disabled(isLoading || addingItemId != nil)
                }
            }
        }
    }

    // MARK: - 搜索内容
    /// 调用后端统一搜索 API
    private func searchContent() async {
        // 重置状态
        errorMessage = nil
        isLoading = true
        showResults = false

        defer {
            isLoading = false
        }

        do {
            // 调用统一搜索 API
            let response = try await APIManager.shared.search(
                query: inputText,
                scope: .tmdb
            )
            print("搜索成功: 找到 \(response.totalResults) 个结果")

            // 更新搜索结果
            searchResults = response.results
            showResults = true

        } catch let error as APIError {
            errorMessage = error.errorDescription
        } catch {
            errorMessage = "搜索失败: \(error.localizedDescription)"
        }
    }

    // MARK: - 添加媒体到收藏
    /// 将选中的媒体添加到数据库
    private func addMedia(_ item: TMDBMediaItem) async {
        // 避免重复添加
        guard addingItemId == nil else { return }

        addingItemId = item.id
        errorMessage = nil

        defer {
            addingItemId = nil
        }

        do {
            let response = try await APIManager.shared.addMedia(from: item)
            print("添加成功: \(response.title) (ID: \(response.id))")

            // 标记为已添加
            addedItemIds.insert(item.id)

        } catch let error as APIError {
            errorMessage = "添加失败: \(error.errorDescription ?? "未知错误")"
        } catch {
            errorMessage = "添加失败: \(error.localizedDescription)"
        }
    }
}

// MARK: - 搜索结果行视图
/// 展示单个搜索结果
struct SearchResultRow: View {
    let item: TMDBMediaItem
    let isAdding: Bool
    let isAdded: Bool
    let onSelect: () -> Void

    var body: some View {
        HStack(spacing: 12) {
            // 海报占位图
            RoundedRectangle(cornerRadius: 6)
                .fill(Color.blue.opacity(0.2))
                .frame(width: 50, height: 75)
                .overlay(
                    Image(systemName: "film")
                        .foregroundColor(.blue.opacity(0.5))
                )

            VStack(alignment: .leading, spacing: 4) {
                Text(item.displayTitle)
                    .font(.headline)
                    .foregroundColor(.primary)
                    .lineLimit(2)

                if let date = item.releaseDate ?? item.firstAirDate {
                    Text(date)
                        .font(.caption)
                        .foregroundColor(.secondary)
                }

                if let overview = item.overview, !overview.isEmpty {
                    Text(overview)
                        .font(.caption)
                        .foregroundColor(.secondary)
                        .lineLimit(2)
                }
            }

            Spacer()

            // 添加按钮
            Button(action: onSelect) {
                if isAdding {
                    ProgressView()
                        .scaleEffect(0.8)
                } else if isAdded {
                    Image(systemName: "checkmark.circle.fill")
                        .foregroundColor(.green)
                        .font(.title2)
                } else {
                    Image(systemName: "plus.circle")
                        .foregroundColor(.blue)
                        .font(.title2)
                }
            }
            .disabled(isAdding || isAdded)
            .buttonStyle(.plain)
        }
        .padding(.vertical, 4)
    }
}

// MARK: - 媒体详情视图（占位）
/// 媒体详情页视图
/// 展示媒体的完整信息、评论、时间线等
/// 这是一个占位视图，实际功能后续实现
struct MediaDetailView: View {
    /// 要展示的媒体条目
    let item: MediaItem

    /// 环境变量：用于关闭当前视图
    @Environment(\.dismiss) private var dismiss

    var body: some View {
        NavigationStack {
            ScrollView {
                VStack(alignment: .leading, spacing: 20) {
                    // ========================================
                    // 头部：海报和基本信息
                    // ========================================
                    HStack(alignment: .top, spacing: 16) {
                        // 海报占位图
                        RoundedRectangle(cornerRadius: 12)
                            .fill(Color.blue.gradient)
                            .frame(width: 120, height: 160)
                            .overlay(
                                Image(systemName: item.type.iconName)
                                    .font(.largeTitle)
                                    .foregroundColor(.white)
                            )

                        // 基本信息
                        VStack(alignment: .leading, spacing: 8) {
                            Text(item.title)
                                .font(.title2)
                                .fontWeight(.bold)

                            Text(item.type.displayName)
                                .font(.subheadline)
                                .foregroundColor(.secondary)

                            if let dateString = item.releaseDateString {
                                Text(dateString)
                                    .font(.subheadline)
                                    .foregroundColor(.secondary)
                            }

                            // 状态标签
                            HStack {
                                if item.isComingSoon {
                                    StatusBadge(text: "即将上映", color: .green)
                                }
                                if item.isEndingSoon {
                                    StatusBadge(text: "即将下映", color: .red)
                                }
                                if item.isNowShowing && !item.isComingSoon && !item.isEndingSoon {
                                    StatusBadge(text: "热映中", color: .orange)
                                }
                            }

                            Spacer()
                        }
                    }
                    .padding()

                    Divider()

                    // ========================================
                    // 用户评分区域
                    // ========================================
                    VStack(alignment: .leading, spacing: 12) {
                        Text("我的评分")
                            .font(.headline)

                        HStack {
                            // 评分星星（占位）
                            ForEach(1...5, id: \.self) { star in
                                Image(systemName: star <= Int((item.userScore ?? 0) / 2) ? "star.fill" : "star")
                                    .foregroundColor(.yellow)
                                    .font(.title2)
                            }

                            Spacer()

                            if let score = item.userScore {
                                Text(String(format: "%.1f", score))
                                    .font(.title)
                                    .fontWeight(.bold)
                            } else {
                                Text("未评分")
                                    .foregroundColor(.secondary)
                            }
                        }
                    }
                    .padding()
                    .background(Color.gray.opacity(0.1))
                    .cornerRadius(12)
                    .padding(.horizontal)

                    // ========================================
                    // 评论区域（占位）
                    // ========================================
                    VStack(alignment: .leading, spacing: 12) {
                        HStack {
                            Text("评论")
                                .font(.headline)
                            Spacer()
                            Button("添加评论") {
                                // TODO: 实现添加评论功能
                            }
                            .font(.subheadline)
                        }

                        // 占位提示
                        Text("暂无评论")
                            .foregroundColor(.secondary)
                            .frame(maxWidth: .infinity, alignment: .center)
                            .padding(.vertical, 40)
                    }
                    .padding()

                    Spacer()
                }
            }
            .navigationTitle("详情")
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .navigationBarTrailing) {
                    Button("完成") {
                        dismiss()
                    }
                }
            }
        }
    }
}

// MARK: - 预览
#Preview("主界面") {
    ContentView()
}

#Preview("添加内容") {
    AddContentView()
}

#Preview("媒体详情") {
    MediaDetailView(item: MediaItem.sampleItems[0])
}
