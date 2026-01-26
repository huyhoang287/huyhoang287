package com.techdoc.manager.data.local.entity

import androidx.room.Entity
import androidx.room.PrimaryKey

/**
 * Room Database Entity cho tài liệu kỹ thuật
 * Lưu trữ thông tin metadata của các file PDF
 */
@Entity(tableName = "documents")
data class Document(
    @PrimaryKey(autoGenerate = true)
    val id: Long = 0,

    val title: String,

    val code: String,

    val category: DocumentCategory,

    val filePath: String,

    val tags: String,

    val dateAdded: Long = System.currentTimeMillis()
)

/**
 * Enum phân loại tài liệu
 */
enum class DocumentCategory {
    STANDARD,
    SPEC,
    MANUAL,
    PROJECT_DOCS,
    CODE
}
