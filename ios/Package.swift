// swift-tools-version: 5.9
import PackageDescription

let package = Package(
    name: "Zoetrope",
    platforms: [
        .iOS(.v16)
    ],
    products: [
        .library(
            name: "Zoetrope",
            targets: ["Zoetrope"]),
    ],
    dependencies: [
        // No external dependencies for now - using native SwiftUI
    ],
    targets: [
        .target(
            name: "Zoetrope",
            dependencies: []),
        .testTarget(
            name: "ZoetropeTests",
            dependencies: ["Zoetrope"]),
    ]
)
