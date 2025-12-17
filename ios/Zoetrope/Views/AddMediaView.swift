import SwiftUI

struct AddMediaView: View {
    @State private var title = ""
    @State private var selectedType = MediaType.movie
    @State private var selectedPriority = PriorityLevel.medium
    @State private var reasonToWatch = ""
    @State private var trailerUrl = ""
    @State private var recommendationText = ""
    @State private var isSubmitting = false
    @State private var showSuccess = false
    @State private var errorMessage: String?
    
    var body: some View {
        NavigationView {
            Form {
                Section(header: Text("基本信息")) {
                    TextField("标题", text: $title)
                    
                    Picker("类型", selection: $selectedType) {
                        ForEach(MediaType.allCases, id: \.self) { type in
                            Text(type.displayName).tag(type)
                        }
                    }
                    
                    Picker("优先级", selection: $selectedPriority) {
                        ForEach(PriorityLevel.allCases, id: \.self) { priority in
                            Text(priority.displayName).tag(priority)
                        }
                    }
                }
                
                Section(header: Text("详细信息")) {
                    TextField("预告片链接", text: $trailerUrl)
                        .keyboardType(.URL)
                        .autocapitalization(.none)
                    
                    TextEditor(text: $reasonToWatch)
                        .frame(minHeight: 80)
                        .overlay(
                            Group {
                                if reasonToWatch.isEmpty {
                                    Text("想看的原因...")
                                        .foregroundColor(.gray.opacity(0.5))
                                        .padding(.horizontal, 4)
                                        .padding(.vertical, 8)
                                        .frame(maxWidth: .infinity, maxHeight: .infinity, alignment: .topLeading)
                                        .allowsHitTesting(false)
                                }
                            }
                        )
                    
                    TextEditor(text: $recommendationText)
                        .frame(minHeight: 80)
                        .overlay(
                            Group {
                                if recommendationText.isEmpty {
                                    Text("推荐文案...")
                                        .foregroundColor(.gray.opacity(0.5))
                                        .padding(.horizontal, 4)
                                        .padding(.vertical, 8)
                                        .frame(maxWidth: .infinity, maxHeight: .infinity, alignment: .topLeading)
                                        .allowsHitTesting(false)
                                }
                            }
                        )
                }
                
                Section {
                    Button(action: submitMedia) {
                        if isSubmitting {
                            ProgressView()
                        } else {
                            Text("添加")
                                .frame(maxWidth: .infinity)
                                .fontWeight(.semibold)
                        }
                    }
                    .disabled(title.isEmpty || isSubmitting)
                }
            }
            .navigationTitle("添加作品")
            .alert("添加成功", isPresented: $showSuccess) {
                Button("确定") {
                    clearForm()
                }
            }
            .alert("错误", isPresented: .constant(errorMessage != nil)) {
                Button("确定") {
                    errorMessage = nil
                }
            } message: {
                if let error = errorMessage {
                    Text(error)
                }
            }
        }
    }
    
    private func submitMedia() {
        guard !title.isEmpty else { return }
        
        isSubmitting = true
        errorMessage = nil
        
        Task {
            do {
                let newMedia = MediaItemCreate(
                    title: title,
                    mediaType: selectedType,
                    reasonToWatch: reasonToWatch.isEmpty ? nil : reasonToWatch,
                    trailerUrl: trailerUrl.isEmpty ? nil : trailerUrl,
                    recommendationText: recommendationText.isEmpty ? nil : recommendationText,
                    priority: selectedPriority
                )
                
                _ = try await APIService.shared.createMediaItem(newMedia)
                
                await MainActor.run {
                    isSubmitting = false
                    showSuccess = true
                }
            } catch {
                await MainActor.run {
                    isSubmitting = false
                    errorMessage = "添加失败: \(error.localizedDescription)"
                }
            }
        }
    }
    
    private func clearForm() {
        title = ""
        selectedType = .movie
        selectedPriority = .medium
        reasonToWatch = ""
        trailerUrl = ""
        recommendationText = ""
    }
}

#Preview {
    AddMediaView()
}
