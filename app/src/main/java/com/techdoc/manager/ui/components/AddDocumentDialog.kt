package com.techdoc.manager.ui.components

import android.net.Uri
import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.AttachFile
import androidx.compose.material.icons.filled.Close
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.window.Dialog
import androidx.compose.ui.window.DialogProperties
import com.techdoc.manager.data.local.entity.DocumentCategory

/**
 * Dialog để thêm tài liệu mới
 * Bao gồm form nhập thông tin và chọn file PDF
 */
@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun AddDocumentDialog(
    onDismiss: () -> Unit,
    onConfirm: (uri: Uri, title: String, code: String, category: DocumentCategory, tags: String) -> Unit
) {
    var selectedUri by remember { mutableStateOf<Uri?>(null) }
    var title by remember { mutableStateOf("") }
    var code by remember { mutableStateOf("") }
    var selectedCategory by remember { mutableStateOf(DocumentCategory.STANDARD) }
    var tags by remember { mutableStateOf("") }
    var showCategoryDropdown by remember { mutableStateOf(false) }

    var titleError by remember { mutableStateOf(false) }
    var codeError by remember { mutableStateOf(false) }
    var fileError by remember { mutableStateOf(false) }

    // File picker launcher
    val filePickerLauncher = rememberLauncherForActivityResult(
        contract = ActivityResultContracts.OpenDocument()
    ) { uri ->
        uri?.let {
            selectedUri = it
            fileError = false
        }
    }

    Dialog(
        onDismissRequest = onDismiss,
        properties = DialogProperties(
            dismissOnBackPress = true,
            dismissOnClickOutside = false,
            usePlatformDefaultWidth = false
        )
    ) {
        Card(
            modifier = Modifier
                .fillMaxWidth(0.95f)
                .fillMaxHeight(0.85f),
            colors = CardDefaults.cardColors(
                containerColor = MaterialTheme.colorScheme.surface
            )
        ) {
            Column(
                modifier = Modifier.fillMaxSize()
            ) {
                // Header
                TopAppBar(
                    title = {
                        Text(
                            text = "Thêm tài liệu mới",
                            fontWeight = FontWeight.Bold
                        )
                    },
                    navigationIcon = {
                        IconButton(onClick = onDismiss) {
                            Icon(
                                imageVector = Icons.Default.Close,
                                contentDescription = "Đóng"
                            )
                        }
                    },
                    colors = TopAppBarDefaults.topAppBarColors(
                        containerColor = MaterialTheme.colorScheme.surface
                    )
                )

                HorizontalDivider()

                // Form content
                Column(
                    modifier = Modifier
                        .weight(1f)
                        .verticalScroll(rememberScrollState())
                        .padding(16.dp),
                    verticalArrangement = Arrangement.spacedBy(16.dp)
                ) {
                    // File picker button
                    OutlinedCard(
                        onClick = {
                            filePickerLauncher.launch(arrayOf("application/pdf"))
                        },
                        modifier = Modifier.fillMaxWidth(),
                        colors = CardDefaults.outlinedCardColors(
                            containerColor = if (fileError)
                                MaterialTheme.colorScheme.errorContainer.copy(alpha = 0.3f)
                            else
                                MaterialTheme.colorScheme.surfaceVariant
                        )
                    ) {
                        Row(
                            modifier = Modifier
                                .fillMaxWidth()
                                .padding(16.dp),
                            verticalAlignment = Alignment.CenterVertically
                        ) {
                            Icon(
                                imageVector = Icons.Default.AttachFile,
                                contentDescription = null,
                                tint = if (selectedUri != null)
                                    MaterialTheme.colorScheme.primary
                                else
                                    MaterialTheme.colorScheme.onSurfaceVariant
                            )
                            Spacer(modifier = Modifier.width(12.dp))
                            Column(modifier = Modifier.weight(1f)) {
                                Text(
                                    text = if (selectedUri != null) "File đã chọn" else "Chọn file PDF",
                                    style = MaterialTheme.typography.bodyLarge,
                                    fontWeight = FontWeight.Medium
                                )
                                if (selectedUri != null) {
                                    Text(
                                        text = selectedUri.toString().substringAfterLast("/"),
                                        style = MaterialTheme.typography.bodySmall,
                                        color = MaterialTheme.colorScheme.onSurfaceVariant
                                    )
                                }
                            }
                        }
                    }
                    if (fileError) {
                        Text(
                            text = "Vui lòng chọn file PDF",
                            color = MaterialTheme.colorScheme.error,
                            style = MaterialTheme.typography.bodySmall
                        )
                    }

                    // Title input
                    OutlinedTextField(
                        value = title,
                        onValueChange = {
                            title = it
                            titleError = false
                        },
                        label = { Text("Tên tài liệu *") },
                        placeholder = { Text("VD: ASME BPVC Section IX - 2023") },
                        modifier = Modifier.fillMaxWidth(),
                        singleLine = true,
                        isError = titleError,
                        supportingText = if (titleError) {
                            { Text("Vui lòng nhập tên tài liệu") }
                        } else null
                    )

                    // Code input
                    OutlinedTextField(
                        value = code,
                        onValueChange = {
                            code = it
                            codeError = false
                        },
                        label = { Text("Mã tiêu chuẩn *") },
                        placeholder = { Text("VD: ASME IX, AWS D1.1, API 650") },
                        modifier = Modifier.fillMaxWidth(),
                        singleLine = true,
                        isError = codeError,
                        supportingText = if (codeError) {
                            { Text("Vui lòng nhập mã tiêu chuẩn") }
                        } else null
                    )

                    // Category dropdown
                    ExposedDropdownMenuBox(
                        expanded = showCategoryDropdown,
                        onExpandedChange = { showCategoryDropdown = it }
                    ) {
                        OutlinedTextField(
                            value = getCategoryDisplayName(selectedCategory),
                            onValueChange = {},
                            readOnly = true,
                            label = { Text("Phân loại") },
                            trailingIcon = {
                                ExposedDropdownMenuDefaults.TrailingIcon(expanded = showCategoryDropdown)
                            },
                            modifier = Modifier
                                .fillMaxWidth()
                                .menuAnchor()
                        )
                        ExposedDropdownMenu(
                            expanded = showCategoryDropdown,
                            onDismissRequest = { showCategoryDropdown = false }
                        ) {
                            DocumentCategory.values().forEach { category ->
                                DropdownMenuItem(
                                    text = { Text(getCategoryDisplayName(category)) },
                                    onClick = {
                                        selectedCategory = category
                                        showCategoryDropdown = false
                                    }
                                )
                            }
                        }
                    }

                    // Tags input
                    OutlinedTextField(
                        value = tags,
                        onValueChange = { tags = it },
                        label = { Text("Tags (từ khóa tìm kiếm)") },
                        placeholder = { Text("VD: welding, qualification, PQR, WPS") },
                        modifier = Modifier.fillMaxWidth(),
                        singleLine = false,
                        minLines = 2,
                        supportingText = { Text("Phân cách bằng dấu phẩy") }
                    )
                }

                HorizontalDivider()

                // Action buttons
                Row(
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(16.dp),
                    horizontalArrangement = Arrangement.End,
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    TextButton(onClick = onDismiss) {
                        Text("Hủy")
                    }
                    Spacer(modifier = Modifier.width(8.dp))
                    Button(
                        onClick = {
                            // Validate
                            var hasError = false
                            if (selectedUri == null) {
                                fileError = true
                                hasError = true
                            }
                            if (title.isBlank()) {
                                titleError = true
                                hasError = true
                            }
                            if (code.isBlank()) {
                                codeError = true
                                hasError = true
                            }

                            if (!hasError && selectedUri != null) {
                                onConfirm(selectedUri!!, title.trim(), code.trim(), selectedCategory, tags.trim())
                            }
                        }
                    ) {
                        Text("Lưu tài liệu")
                    }
                }
            }
        }
    }
}

/**
 * Lấy tên hiển thị của category
 */
private fun getCategoryDisplayName(category: DocumentCategory): String {
    return when (category) {
        DocumentCategory.STANDARD -> "Standard (Tiêu chuẩn)"
        DocumentCategory.SPEC -> "Specification (Quy cách)"
        DocumentCategory.MANUAL -> "Manual (Hướng dẫn)"
        DocumentCategory.PROJECT_DOCS -> "Project Docs (Tài liệu dự án)"
        DocumentCategory.CODE -> "Code (Quy phạm)"
    }
}
