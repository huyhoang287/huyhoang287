package com.techdoc.manager.data.repository

import com.techdoc.manager.data.local.dao.DocumentDao
import com.techdoc.manager.data.local.entity.Document
import com.techdoc.manager.data.local.entity.DocumentCategory
import kotlinx.coroutines.flow.Flow

/**
 * Repository pattern để quản lý nguồn dữ liệu
 * Cung cấp abstraction layer giữa ViewModel và Data Source
 */
class DocumentRepository(private val documentDao: DocumentDao) {

    val allDocuments: Flow<List<Document>> = documentDao.getAllDocuments()

    val documentCount: Flow<Int> = documentDao.getDocumentCount()

    fun searchDocuments(query: String): Flow<List<Document>> {
        return documentDao.searchDocuments(query)
    }

    fun getDocumentsByCategory(category: DocumentCategory): Flow<List<Document>> {
        return documentDao.getDocumentsByCategory(category)
    }

    suspend fun getDocumentById(id: Long): Document? {
        return documentDao.getDocumentById(id)
    }

    suspend fun insertDocument(document: Document): Long {
        return documentDao.insertDocument(document)
    }

    suspend fun updateDocument(document: Document) {
        documentDao.updateDocument(document)
    }

    suspend fun deleteDocument(document: Document) {
        documentDao.deleteDocument(document)
    }

    suspend fun deleteDocumentById(id: Long) {
        documentDao.deleteDocumentById(id)
    }
}
