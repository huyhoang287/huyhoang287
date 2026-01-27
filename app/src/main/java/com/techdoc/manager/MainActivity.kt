package com.techdoc.manager

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.ui.Modifier
import androidx.navigation.compose.rememberNavController
import com.techdoc.manager.navigation.TechDocNavGraph
import com.techdoc.manager.ui.theme.TechDocManagerTheme

/**
 * Activity chính của ứng dụng TechDoc Manager
 * Quản lý tài liệu kỹ thuật PDF cho Kỹ sư, QC Inspector, Welder
 */
class MainActivity : ComponentActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()

        setContent {
            TechDocManagerTheme {
                Surface(
                    modifier = Modifier.fillMaxSize(),
                    color = MaterialTheme.colorScheme.background
                ) {
                    val navController = rememberNavController()
                    TechDocNavGraph(navController = navController)
                }
            }
        }
    }
}
