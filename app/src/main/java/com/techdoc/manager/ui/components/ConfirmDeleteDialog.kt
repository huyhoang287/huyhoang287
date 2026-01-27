package com.techdoc.manager.ui.components

import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.ui.text.font.FontWeight
import com.techdoc.manager.data.local.entity.Document

/**
 * Dialog xác nhận xóa tài liệu
 */
@Composable
fun ConfirmDeleteDialog(
    document: Document,
    onConfirm: () -> Unit,
    onDismiss: () -> Unit
) {
    AlertDialog(
        onDismissRequest = onDismiss,
        title = {
            Text(
                text = "Xác nhận xóa",
                fontWeight = FontWeight.Bold
            )
        },
        text = {
            Text(
                text = "Bạn có chắc chắn muốn xóa tài liệu \"${document.title}\"?\n\nHành động này không thể hoàn tác."
            )
        },
        confirmButton = {
            TextButton(
                onClick = onConfirm,
                colors = ButtonDefaults.textButtonColors(
                    contentColor = MaterialTheme.colorScheme.error
                )
            ) {
                Text("Xóa")
            }
        },
        dismissButton = {
            TextButton(onClick = onDismiss) {
                Text("Hủy")
            }
        }
    )
}
