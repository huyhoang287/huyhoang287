package com.techdoc.manager.ui.components

import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Delete
import androidx.compose.material.icons.filled.Description
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import com.techdoc.manager.data.local.entity.Document
import com.techdoc.manager.data.local.entity.DocumentCategory
import java.text.SimpleDateFormat
import java.util.*

/**
 * Card hiển thị thông tin tài liệu trong danh sách
 */
@Composable
fun DocumentCard(
    document: Document,
    onClick: () -> Unit,
    onDeleteClick: () -> Unit,
    modifier: Modifier = Modifier
) {
    Card(
        modifier = modifier
            .fillMaxWidth()
            .clickable(onClick = onClick),
        colors = CardDefaults.cardColors(
            containerColor = MaterialTheme.colorScheme.surfaceVariant
        ),
        elevation = CardDefaults.cardElevation(defaultElevation = 2.dp)
    ) {
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .padding(16.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            // Icon PDF
            Icon(
                imageVector = Icons.Default.Description,
                contentDescription = null,
                modifier = Modifier.size(48.dp),
                tint = MaterialTheme.colorScheme.primary
            )

            Spacer(modifier = Modifier.width(16.dp))

            // Thông tin tài liệu
            Column(
                modifier = Modifier.weight(1f)
            ) {
                Text(
                    text = document.title,
                    style = MaterialTheme.typography.titleMedium,
                    fontWeight = FontWeight.Bold,
                    maxLines = 2,
                    overflow = TextOverflow.Ellipsis,
                    color = MaterialTheme.colorScheme.onSurface
                )

                Spacer(modifier = Modifier.height(4.dp))

                Row(
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    // Mã tiêu chuẩn
                    AssistChip(
                        onClick = { },
                        label = {
                            Text(
                                text = document.code,
                                style = MaterialTheme.typography.labelSmall
                            )
                        },
                        colors = AssistChipDefaults.assistChipColors(
                            containerColor = MaterialTheme.colorScheme.primaryContainer
                        )
                    )

                    Spacer(modifier = Modifier.width(8.dp))

                    // Category badge
                    CategoryBadge(category = document.category)
                }

                Spacer(modifier = Modifier.height(4.dp))

                // Tags
                if (document.tags.isNotBlank()) {
                    Text(
                        text = document.tags,
                        style = MaterialTheme.typography.bodySmall,
                        color = MaterialTheme.colorScheme.onSurfaceVariant,
                        maxLines = 1,
                        overflow = TextOverflow.Ellipsis
                    )
                }

                Spacer(modifier = Modifier.height(4.dp))

                // Ngày thêm
                Text(
                    text = formatDate(document.dateAdded),
                    style = MaterialTheme.typography.labelSmall,
                    color = MaterialTheme.colorScheme.onSurfaceVariant
                )
            }

            // Nút xóa
            IconButton(onClick = onDeleteClick) {
                Icon(
                    imageVector = Icons.Default.Delete,
                    contentDescription = "Xóa tài liệu",
                    tint = MaterialTheme.colorScheme.error
                )
            }
        }
    }
}

/**
 * Badge hiển thị category
 */
@Composable
fun CategoryBadge(category: DocumentCategory) {
    val (text, containerColor) = when (category) {
        DocumentCategory.STANDARD -> "Standard" to MaterialTheme.colorScheme.secondary
        DocumentCategory.SPEC -> "Spec" to MaterialTheme.colorScheme.tertiary
        DocumentCategory.MANUAL -> "Manual" to MaterialTheme.colorScheme.primary
        DocumentCategory.PROJECT_DOCS -> "Project" to MaterialTheme.colorScheme.secondary
        DocumentCategory.CODE -> "Code" to MaterialTheme.colorScheme.tertiary
    }

    Surface(
        color = containerColor,
        shape = MaterialTheme.shapes.small
    ) {
        Text(
            text = text,
            modifier = Modifier.padding(horizontal = 8.dp, vertical = 4.dp),
            style = MaterialTheme.typography.labelSmall,
            color = MaterialTheme.colorScheme.onSecondary
        )
    }
}

/**
 * Format timestamp thành chuỗi ngày tháng
 */
private fun formatDate(timestamp: Long): String {
    val dateFormat = SimpleDateFormat("dd/MM/yyyy", Locale.getDefault())
    return dateFormat.format(Date(timestamp))
}
