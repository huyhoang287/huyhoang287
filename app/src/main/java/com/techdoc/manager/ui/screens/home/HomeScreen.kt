package com.techdoc.manager.ui.screens.home

import androidx.compose.animation.AnimatedVisibility
import androidx.compose.animation.fadeIn
import androidx.compose.animation.fadeOut
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.LazyRow
import androidx.compose.foundation.lazy.items
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Add
import androidx.compose.material.icons.filled.Clear
import androidx.compose.material.icons.filled.Search
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import com.techdoc.manager.data.local.entity.Document
import com.techdoc.manager.data.local.entity.DocumentCategory
import com.techdoc.manager.ui.components.ConfirmDeleteDialog
import com.techdoc.manager.ui.components.DocumentCard
import com.techdoc.manager.viewmodel.HomeUiState
import com.techdoc.manager.viewmodel.HomeViewModel

/**
 * Màn hình chính hiển thị danh sách tài liệu
 * Sử dụng Material 3 Design với hỗ trợ Dark Mode
 */
@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun HomeScreen(
    viewModel: HomeViewModel,
    onDocumentClick: (Document) -> Unit,
    onAddClick: () -> Unit
) {
    val documents by viewModel.documents.collectAsState()
    val searchQuery by viewModel.searchQuery.collectAsState()
    val selectedCategory by viewModel.selectedCategory.collectAsState()
    val isLoading by viewModel.isLoading.collectAsState()
    val uiState by viewModel.uiState.collectAsState()

    // Delete confirmation dialog state
    var documentToDelete by remember { mutableStateOf<Document?>(null) }

    // Show delete confirmation dialog
    documentToDelete?.let { document ->
        ConfirmDeleteDialog(
            document = document,
            onConfirm = {
                viewModel.deleteDocument(document)
                documentToDelete = null
            },
            onDismiss = {
                documentToDelete = null
            }
        )
    }

    Scaffold(
        topBar = {
            HomeTopBar(
                searchQuery = searchQuery,
                onSearchQueryChange = viewModel::updateSearchQuery,
                onClearSearch = { viewModel.updateSearchQuery("") }
            )
        },
        floatingActionButton = {
            FloatingActionButton(
                onClick = onAddClick,
                containerColor = MaterialTheme.colorScheme.primary,
                contentColor = MaterialTheme.colorScheme.onPrimary
            ) {
                Icon(
                    imageVector = Icons.Default.Add,
                    contentDescription = "Thêm tài liệu mới"
                )
            }
        }
    ) { paddingValues ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(paddingValues)
        ) {
            // Category Filter Chips
            CategoryFilterRow(
                selectedCategory = selectedCategory,
                onCategorySelected = viewModel::selectCategory
            )

            // Loading indicator
            AnimatedVisibility(
                visible = isLoading,
                enter = fadeIn(),
                exit = fadeOut()
            ) {
                LinearProgressIndicator(
                    modifier = Modifier.fillMaxWidth()
                )
            }

            // Main content
            when (uiState) {
                is HomeUiState.Loading -> {
                    LoadingContent()
                }
                is HomeUiState.Empty -> {
                    EmptyContent(
                        hasFilter = searchQuery.isNotBlank() || selectedCategory != null,
                        onClearFilters = viewModel::clearFilters
                    )
                }
                is HomeUiState.Success -> {
                    DocumentList(
                        documents = documents,
                        onDocumentClick = onDocumentClick,
                        onDeleteClick = { document ->
                            documentToDelete = document
                        }
                    )
                }
                is HomeUiState.Error -> {
                    ErrorContent(message = (uiState as HomeUiState.Error).message)
                }
            }
        }
    }
}

/**
 * TopAppBar với thanh tìm kiếm
 */
@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun HomeTopBar(
    searchQuery: String,
    onSearchQueryChange: (String) -> Unit,
    onClearSearch: () -> Unit
) {
    var isSearchActive by remember { mutableStateOf(false) }

    TopAppBar(
        title = {
            if (isSearchActive) {
                OutlinedTextField(
                    value = searchQuery,
                    onValueChange = onSearchQueryChange,
                    placeholder = {
                        Text("Tìm kiếm theo tên, mã, tag...")
                    },
                    singleLine = true,
                    modifier = Modifier.fillMaxWidth(),
                    colors = OutlinedTextFieldDefaults.colors(
                        focusedBorderColor = MaterialTheme.colorScheme.primary,
                        unfocusedBorderColor = MaterialTheme.colorScheme.outline
                    ),
                    trailingIcon = {
                        if (searchQuery.isNotBlank()) {
                            IconButton(onClick = onClearSearch) {
                                Icon(
                                    imageVector = Icons.Default.Clear,
                                    contentDescription = "Xóa tìm kiếm"
                                )
                            }
                        }
                    }
                )
            } else {
                Text(
                    text = "TechDoc Manager",
                    style = MaterialTheme.typography.headlineSmall,
                    fontWeight = FontWeight.Bold
                )
            }
        },
        actions = {
            IconButton(
                onClick = {
                    isSearchActive = !isSearchActive
                    if (!isSearchActive) {
                        onClearSearch()
                    }
                }
            ) {
                Icon(
                    imageVector = if (isSearchActive) Icons.Default.Clear else Icons.Default.Search,
                    contentDescription = if (isSearchActive) "Đóng tìm kiếm" else "Tìm kiếm"
                )
            }
        },
        colors = TopAppBarDefaults.topAppBarColors(
            containerColor = MaterialTheme.colorScheme.surface,
            titleContentColor = MaterialTheme.colorScheme.onSurface
        )
    )
}

/**
 * Hàng filter theo category
 */
@Composable
fun CategoryFilterRow(
    selectedCategory: DocumentCategory?,
    onCategorySelected: (DocumentCategory?) -> Unit
) {
    LazyRow(
        modifier = Modifier
            .fillMaxWidth()
            .padding(horizontal = 16.dp, vertical = 8.dp),
        horizontalArrangement = Arrangement.spacedBy(8.dp)
    ) {
        item {
            FilterChip(
                selected = selectedCategory == null,
                onClick = { onCategorySelected(null) },
                label = { Text("Tất cả") },
                colors = FilterChipDefaults.filterChipColors(
                    selectedContainerColor = MaterialTheme.colorScheme.primaryContainer
                )
            )
        }

        items(DocumentCategory.values()) { category ->
            FilterChip(
                selected = selectedCategory == category,
                onClick = { onCategorySelected(category) },
                label = { Text(getCategoryDisplayName(category)) },
                colors = FilterChipDefaults.filterChipColors(
                    selectedContainerColor = MaterialTheme.colorScheme.primaryContainer
                )
            )
        }
    }
}

/**
 * Lấy tên hiển thị của category
 */
fun getCategoryDisplayName(category: DocumentCategory): String {
    return when (category) {
        DocumentCategory.STANDARD -> "Standard"
        DocumentCategory.SPEC -> "Specification"
        DocumentCategory.MANUAL -> "Manual"
        DocumentCategory.PROJECT_DOCS -> "Project Docs"
        DocumentCategory.CODE -> "Code"
    }
}

/**
 * Danh sách tài liệu sử dụng LazyColumn
 */
@Composable
fun DocumentList(
    documents: List<Document>,
    onDocumentClick: (Document) -> Unit,
    onDeleteClick: (Document) -> Unit
) {
    LazyColumn(
        modifier = Modifier.fillMaxSize(),
        contentPadding = PaddingValues(16.dp),
        verticalArrangement = Arrangement.spacedBy(12.dp)
    ) {
        items(
            items = documents,
            key = { it.id }
        ) { document ->
            DocumentCard(
                document = document,
                onClick = { onDocumentClick(document) },
                onDeleteClick = { onDeleteClick(document) }
            )
        }
    }
}

/**
 * Nội dung hiển thị khi đang loading
 */
@Composable
fun LoadingContent() {
    Box(
        modifier = Modifier.fillMaxSize(),
        contentAlignment = Alignment.Center
    ) {
        CircularProgressIndicator()
    }
}

/**
 * Nội dung hiển thị khi không có tài liệu
 */
@Composable
fun EmptyContent(
    hasFilter: Boolean,
    onClearFilters: () -> Unit
) {
    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(32.dp),
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.Center
    ) {
        Text(
            text = if (hasFilter) "Không tìm thấy tài liệu" else "Chưa có tài liệu nào",
            style = MaterialTheme.typography.headlineSmall,
            textAlign = TextAlign.Center,
            color = MaterialTheme.colorScheme.onSurfaceVariant
        )

        Spacer(modifier = Modifier.height(8.dp))

        Text(
            text = if (hasFilter) {
                "Thử thay đổi bộ lọc hoặc từ khóa tìm kiếm"
            } else {
                "Nhấn nút (+) để thêm tài liệu kỹ thuật đầu tiên"
            },
            style = MaterialTheme.typography.bodyMedium,
            textAlign = TextAlign.Center,
            color = MaterialTheme.colorScheme.onSurfaceVariant
        )

        if (hasFilter) {
            Spacer(modifier = Modifier.height(16.dp))

            OutlinedButton(onClick = onClearFilters) {
                Text("Xóa bộ lọc")
            }
        }
    }
}

/**
 * Nội dung hiển thị khi có lỗi
 */
@Composable
fun ErrorContent(message: String) {
    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(32.dp),
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.Center
    ) {
        Text(
            text = "Đã xảy ra lỗi",
            style = MaterialTheme.typography.headlineSmall,
            color = MaterialTheme.colorScheme.error
        )

        Spacer(modifier = Modifier.height(8.dp))

        Text(
            text = message,
            style = MaterialTheme.typography.bodyMedium,
            textAlign = TextAlign.Center,
            color = MaterialTheme.colorScheme.onSurfaceVariant
        )
    }
}
