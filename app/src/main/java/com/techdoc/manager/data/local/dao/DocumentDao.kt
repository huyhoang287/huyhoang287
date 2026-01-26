package com.techdoc.manager.data.local.dao

import androidx.room.*
import com.techdoc.manager.data.local.entity.Document
import com.techdoc.manager.data.local.entity.DocumentCategory
import kotlinx.coroutines.flow.Flow

/**
 * Data Access Object cho thao tác với bảng documents
 */
@Dao
interface DocumentDao {

    /**
     * Lấy tất cả tài liệu, sắp xếp theo ngày thêm mới nhất
     */
    @Query("SELECT * FROM documents ORDER BY dateAdded DESC")
    fun getAllDocuments(): Flow<List<Document>>

    /**
     * Tìm kiếm tài liệu theo tên, mã hoặc tags
     */
    @Query("""
        SELECT * FROM documents
        WHERE title LIKE '%' || :query || '%'
        OR code LIKE '%' || :query || '%'
        OR tags LIKE '%' || :query || '%'
        ORDER BY dateAdded DESC
    """)
    fun searchDocuments(query: String): Flow<List<Document>>

    /**
     * Lọc tài liệu theo category
     */
    @Query("SELECT * FROM documents WHERE category = :category ORDER BY dateAdded DESC")
    fun getDocumentsByCategory(category: DocumentCategory): Flow<List<Document>>

    /**
     * Lấy một tài liệu theo ID
     */
    @Query("SELECT * FROM documents WHERE id = :id")
    suspend fun getDocumentById(id: Long): Document?

    /**
     * Thêm tài liệu mới
     */
    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertDocument(document: Document): Long

    /**
     * Cập nhật thông tin tài liệu
     */
    @Update
    suspend fun updateDocument(document: Document)

    /**
     * Xóa tài liệu
     */
    @Delete
    suspend fun deleteDocument(document: Document)

    /**
     * Xóa tài liệu theo ID
     */
    @Query("DELETE FROM documents WHERE id = :id")
    suspend fun deleteDocumentById(id: Long)

    /**
     * Đếm tổng số tài liệu
     */
    @Query("SELECT COUNT(*) FROM documents")
    fun getDocumentCount(): Flow<Int>
}
