package com.techdoc.manager.viewmodel

import android.app.Application
import android.content.Context
import android.net.Uri
import androidx.lifecycle.AndroidViewModel
import androidx.lifecycle.viewModelScope
import com.techdoc.manager.data.local.database.TechDocDatabase
import com.techdoc.manager.data.local.entity.Document
import com.techdoc.manager.data.local.entity.DocumentCategory
import com.techdoc.manager.data.repository.DocumentRepository
import kotlinx.coroutines.ExperimentalCoroutinesApi
import kotlinx.coroutines.flow.*
import kotlinx.coroutines.launch
import java.io.File
import java.io.FileOutputStream
import java.util.UUID

/**
 * ViewModel cho màn hình Home
 * Quản lý state và business logic cho danh sách tài liệu
 */
class HomeViewModel(application: Application) : AndroidViewModel(application) {

    private val repository: DocumentRepository

    private val _searchQuery = MutableStateFlow("")
    val searchQuery: StateFlow<String> = _searchQuery.asStateFlow()

    private val _selectedCategory = MutableStateFlow<DocumentCategory?>(null)
    val selectedCategory: StateFlow<DocumentCategory?> = _selectedCategory.asStateFlow()

    private val _isLoading = MutableStateFlow(false)
    val isLoading: StateFlow<Boolean> = _isLoading.asStateFlow()

    private val _uiState = MutableStateFlow<HomeUiState>(HomeUiState.Loading)
    val uiState: StateFlow<HomeUiState> = _uiState.asStateFlow()

    @OptIn(ExperimentalCoroutinesApi::class)
    val documents: StateFlow<List<Document>>

    init {
        val database = TechDocDatabase.getInstance(application)
        repository = DocumentRepository(database.documentDao())

        documents = combine(
            _searchQuery,
            _selectedCategory
        ) { query, category ->
            Pair(query, category)
        }.flatMapLatest { (query, category) ->
            when {
                query.isNotBlank() -> repository.searchDocuments(query)
                category != null -> repository.getDocumentsByCategory(category)
                else -> repository.allDocuments
            }
        }.stateIn(
            scope = viewModelScope,
            started = SharingStarted.WhileSubscribed(5000),
            initialValue = emptyList()
        )

        viewModelScope.launch {
            documents.collect { docs ->
                _uiState.value = if (docs.isEmpty() && _searchQuery.value.isBlank()) {
                    HomeUiState.Empty
                } else {
                    HomeUiState.Success(docs)
                }
            }
        }
    }

    fun updateSearchQuery(query: String) {
        _searchQuery.value = query
    }

    fun selectCategory(category: DocumentCategory?) {
        _selectedCategory.value = category
    }

    fun clearFilters() {
        _searchQuery.value = ""
        _selectedCategory.value = null
    }

    /**
     * Import file PDF từ URI vào internal storage
     * Copy file và lưu metadata vào database
     */
    fun importDocument(
        uri: Uri,
        title: String,
        code: String,
        category: DocumentCategory,
        tags: String
    ) {
        viewModelScope.launch {
            _isLoading.value = true
            try {
                val context = getApplication<Application>()
                val filePath = copyFileToInternalStorage(context, uri)

                if (filePath != null) {
                    val document = Document(
                        title = title,
                        code = code,
                        category = category,
                        filePath = filePath,
                        tags = tags
                    )
                    repository.insertDocument(document)
                }
            } catch (e: Exception) {
                e.printStackTrace()
            } finally {
                _isLoading.value = false
            }
        }
    }

    /**
     * Copy file từ URI vào thư mục nội bộ của ứng dụng
     */
    private fun copyFileToInternalStorage(context: Context, uri: Uri): String? {
        return try {
            val inputStream = context.contentResolver.openInputStream(uri)
            val fileName = "${UUID.randomUUID()}.pdf"
            val documentsDir = File(context.filesDir, "documents")

            if (!documentsDir.exists()) {
                documentsDir.mkdirs()
            }

            val destinationFile = File(documentsDir, fileName)

            inputStream?.use { input ->
                FileOutputStream(destinationFile).use { output ->
                    input.copyTo(output)
                }
            }

            destinationFile.absolutePath
        } catch (e: Exception) {
            e.printStackTrace()
            null
        }
    }

    fun deleteDocument(document: Document) {
        viewModelScope.launch {
            try {
                // Xóa file vật lý
                val file = File(document.filePath)
                if (file.exists()) {
                    file.delete()
                }
                // Xóa record trong database
                repository.deleteDocument(document)
            } catch (e: Exception) {
                e.printStackTrace()
            }
        }
    }
}

/**
 * Sealed class đại diện cho các trạng thái UI
 */
sealed class HomeUiState {
    object Loading : HomeUiState()
    object Empty : HomeUiState()
    data class Success(val documents: List<Document>) : HomeUiState()
    data class Error(val message: String) : HomeUiState()
}
