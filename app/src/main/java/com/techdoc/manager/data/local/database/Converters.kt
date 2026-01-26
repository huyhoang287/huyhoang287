package com.techdoc.manager.data.local.database

import androidx.room.TypeConverter
import com.techdoc.manager.data.local.entity.DocumentCategory

/**
 * Type Converters cho Room Database
 * Chuyển đổi các kiểu dữ liệu phức tạp thành kiểu đơn giản để lưu vào SQLite
 */
class Converters {

    @TypeConverter
    fun fromDocumentCategory(category: DocumentCategory): String {
        return category.name
    }

    @TypeConverter
    fun toDocumentCategory(value: String): DocumentCategory {
        return DocumentCategory.valueOf(value)
    }
}
