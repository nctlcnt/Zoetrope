//
//  CarouselView.swift
//  Zoetrope
//
//  轮播区组件
//  用于在主界面上半部分展示推荐内容
//  类似院线贴片广告的轮播效果
//

import SwiftUI

// MARK: - 轮播区主视图
/// 轮播区视图组件
/// 展示最近上映、高热度、AI推荐等内容
/// 支持左右滑动浏览，提供快捷交互按钮
struct CarouselView: View {
    // MARK: 属性

    /// 要展示的媒体条目列表
    /// 应该已经按优先级排序
    let items: [MediaItem]

    /// 当前显示的页面索引
    @State private var currentIndex: Int = 0

    /// 交互回调：用户点击"不感兴趣"
    var onNotInterested: ((MediaItem) -> Void)?

    /// 交互回调：用户点击"稍后再看"
    var onWatchLater: ((MediaItem) -> Void)?

    /// 交互回调：用户点击条目进入详情
    var onItemTapped: ((MediaItem) -> Void)?

    // MARK: 视图主体
    var body: some View {
        VStack(spacing: 12) {
            // ========================================
            // 轮播内容区域
            // 使用TabView实现左右滑动的轮播效果
            // ========================================
            TabView(selection: $currentIndex) {
                // 遍历所有媒体条目，为每个条目创建轮播卡片
                ForEach(Array(items.enumerated()), id: \.element.id) { index, item in
                    CarouselCardView(item: item)
                        .tag(index)  // 用于追踪当前显示的页面
                        .padding(.horizontal, 20)  // 左右留白，露出相邻卡片边缘
                        .onTapGesture {
                            // 点击卡片进入详情页
                            onItemTapped?(item)
                        }
                }
            }
            // 使用页面样式的TabView
            .tabViewStyle(PageTabViewStyle(indexDisplayMode: .never))
            .frame(height: 200)  // 固定轮播区高度

            // ========================================
            // 页面指示器（小圆点）
            // 显示当前浏览位置
            // ========================================
            PageIndicatorView(
                totalPages: items.count,
                currentPage: currentIndex
            )

            // ========================================
            // 快捷操作按钮区域
            // 提供"不感兴趣"和"稍后再看"快捷操作
            // ========================================
            if !items.isEmpty {
                QuickActionsView(
                    onNotInterested: {
                        // 触发"不感兴趣"回调
                        guard currentIndex < items.count else { return }
                        onNotInterested?(items[currentIndex])
                    },
                    onWatchLater: {
                        // 触发"稍后再看"回调
                        guard currentIndex < items.count else { return }
                        onWatchLater?(items[currentIndex])
                    }
                )
            }
        }
        .padding(.vertical, 16)
        // 设置背景，使轮播区在视觉上与列表区分开
        .background(
            LinearGradient(
                colors: [Color.blue.opacity(0.1), Color.purple.opacity(0.1)],
                startPoint: .topLeading,
                endPoint: .bottomTrailing
            )
        )
    }
}

// MARK: - 轮播卡片视图
/// 单个轮播卡片的视图
/// 展示媒体的海报、标题、类型等基本信息
struct CarouselCardView: View {
    /// 要展示的媒体条目
    let item: MediaItem

    var body: some View {
        // 使用ZStack实现图片上叠加文字的效果
        ZStack(alignment: .bottomLeading) {
            // ========================================
            // 背景层：海报图片或占位色块
            // ========================================
            RoundedRectangle(cornerRadius: 16)
                .fill(
                    // 根据媒体类型使用不同的渐变色作为占位背景
                    // 实际项目中这里会显示海报图片
                    LinearGradient(
                        colors: gradientColors(for: item.type),
                        startPoint: .topLeading,
                        endPoint: .bottomTrailing
                    )
                )

            // ========================================
            // 前景层：标题和信息
            // 使用渐变遮罩确保文字可读性
            // ========================================
            VStack(alignment: .leading, spacing: 8) {
                Spacer()

                // 媒体类型标签（如：电影、电视剧）
                HStack(spacing: 4) {
                    Image(systemName: item.type.iconName)
                        .font(.caption)
                    Text(item.type.displayName)
                        .font(.caption)
                        .fontWeight(.medium)
                }
                .padding(.horizontal, 8)
                .padding(.vertical, 4)
                .background(Color.white.opacity(0.2))
                .cornerRadius(8)

                // 媒体标题
                Text(item.title)
                    .font(.title2)
                    .fontWeight(.bold)
                    .foregroundColor(.white)
                    .lineLimit(2)  // 最多显示两行

                // 上映日期或状态标签
                HStack(spacing: 8) {
                    // 显示上映日期
                    if let dateString = item.releaseDateString {
                        Text(dateString)
                            .font(.subheadline)
                            .foregroundColor(.white.opacity(0.8))
                    }

                    // 状态标签：即将上映/即将下映
                    if item.isComingSoon {
                        StatusBadge(text: "即将上映", color: .green)
                    } else if item.isEndingSoon {
                        StatusBadge(text: "即将下映", color: .red)
                    } else if item.isNowShowing {
                        StatusBadge(text: "热映中", color: .orange)
                    }
                }
            }
            .padding(16)
            // 底部渐变遮罩，确保文字可读
            .frame(maxWidth: .infinity, alignment: .leading)
            .background(
                LinearGradient(
                    colors: [.clear, .black.opacity(0.7)],
                    startPoint: .top,
                    endPoint: .bottom
                )
            )
            .cornerRadius(16)
        }
        // 添加阴影效果增加层次感
        .shadow(color: .black.opacity(0.2), radius: 10, x: 0, y: 5)
    }

    // MARK: 辅助方法

    /// 根据媒体类型返回对应的渐变色
    /// - Parameter type: 媒体类型
    /// - Returns: 渐变色数组
    private func gradientColors(for type: MediaType) -> [Color] {
        switch type {
        case .movie:
            return [Color.blue, Color.purple]
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

// MARK: - 状态标签组件
/// 小型状态标签，用于显示"即将上映"、"即将下映"等状态
struct StatusBadge: View {
    let text: String
    let color: Color

    var body: some View {
        Text(text)
            .font(.caption2)
            .fontWeight(.semibold)
            .foregroundColor(.white)
            .padding(.horizontal, 6)
            .padding(.vertical, 2)
            .background(color)
            .cornerRadius(4)
    }
}

// MARK: - 页面指示器
/// 显示当前页面位置的小圆点指示器
struct PageIndicatorView: View {
    /// 总页数
    let totalPages: Int

    /// 当前页码（从0开始）
    let currentPage: Int

    var body: some View {
        HStack(spacing: 8) {
            // 为每一页创建一个指示点
            ForEach(0..<totalPages, id: \.self) { index in
                Circle()
                    .fill(index == currentPage ? Color.primary : Color.gray.opacity(0.5))
                    // 当前页的指示点稍大
                    .frame(width: index == currentPage ? 8 : 6,
                           height: index == currentPage ? 8 : 6)
                    // 添加切换动画
                    .animation(.easeInOut(duration: 0.2), value: currentPage)
            }
        }
    }
}

// MARK: - 快捷操作按钮
/// 轮播区下方的快捷操作按钮
/// 提供"不感兴趣"和"稍后再看"两个常用操作
struct QuickActionsView: View {
    /// "不感兴趣"按钮点击回调
    var onNotInterested: (() -> Void)?

    /// "稍后再看"按钮点击回调
    var onWatchLater: (() -> Void)?

    var body: some View {
        HStack(spacing: 20) {
            // "不感兴趣"按钮
            // 点击后会降低该条目的优先级
            Button(action: { onNotInterested?() }) {
                HStack(spacing: 4) {
                    Image(systemName: "hand.thumbsdown")
                    Text("不感兴趣")
                }
                .font(.subheadline)
                .foregroundColor(.secondary)
                .padding(.horizontal, 12)
                .padding(.vertical, 8)
                .background(Color.gray.opacity(0.1))
                .cornerRadius(20)
            }

            // "稍后再看"按钮
            // 点击后会调整该条目的排序
            Button(action: { onWatchLater?() }) {
                HStack(spacing: 4) {
                    Image(systemName: "clock")
                    Text("稍后再看")
                }
                .font(.subheadline)
                .foregroundColor(.secondary)
                .padding(.horizontal, 12)
                .padding(.vertical, 8)
                .background(Color.gray.opacity(0.1))
                .cornerRadius(20)
            }
        }
    }
}

// MARK: - 预览
#Preview("轮播区") {
    CarouselView(items: MediaItem.sampleItems)
}

#Preview("轮播卡片") {
    CarouselCardView(item: MediaItem.sampleItems[0])
        .frame(height: 200)
        .padding()
}
