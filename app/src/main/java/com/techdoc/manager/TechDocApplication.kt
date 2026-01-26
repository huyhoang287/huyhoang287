package com.techdoc.manager

import android.app.Application
import com.techdoc.manager.data.local.database.TechDocDatabase

/**
 * Application class cho TechDoc Manager
 * Khởi tạo các dependencies toàn cục
 */
class TechDocApplication : Application() {

    val database: TechDocDatabase by lazy {
        TechDocDatabase.getInstance(this)
    }

    override fun onCreate() {
        super.onCreate()
        instance = this
    }

    companion object {
        lateinit var instance: TechDocApplication
            private set
    }
}
