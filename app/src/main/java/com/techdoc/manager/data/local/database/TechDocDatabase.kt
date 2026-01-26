package com.techdoc.manager.data.local.database

import android.content.Context
import androidx.room.Database
import androidx.room.Room
import androidx.room.RoomDatabase
import androidx.room.TypeConverters
import com.techdoc.manager.data.local.dao.DocumentDao
import com.techdoc.manager.data.local.entity.Document

/**
 * Room Database chính của ứng dụng TechDoc Manager
 */
@Database(
    entities = [Document::class],
    version = 1,
    exportSchema = false
)
@TypeConverters(Converters::class)
abstract class TechDocDatabase : RoomDatabase() {

    abstract fun documentDao(): DocumentDao

    companion object {
        private const val DATABASE_NAME = "techdoc_database"

        @Volatile
        private var INSTANCE: TechDocDatabase? = null

        fun getInstance(context: Context): TechDocDatabase {
            return INSTANCE ?: synchronized(this) {
                val instance = Room.databaseBuilder(
                    context.applicationContext,
                    TechDocDatabase::class.java,
                    DATABASE_NAME
                )
                    .fallbackToDestructiveMigration()
                    .build()
                INSTANCE = instance
                instance
            }
        }
    }
}
