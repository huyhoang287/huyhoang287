package com.techdoc.manager

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.activity.viewModels
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.ui.Modifier
import com.techdoc.manager.ui.screens.home.HomeScreen
import com.techdoc.manager.ui.theme.TechDocManagerTheme
import com.techdoc.manager.viewmodel.HomeViewModel

/**
 * Activity chính của ứng dụng TechDoc Manager
 */
class MainActivity : ComponentActivity() {

    private val homeViewModel: HomeViewModel by viewModels()

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()

        setContent {
            TechDocManagerTheme {
                Surface(
                    modifier = Modifier.fillMaxSize(),
                    color = MaterialTheme.colorScheme.background
                ) {
                    HomeScreen(
                        viewModel = homeViewModel,
                        onDocumentClick = { document ->
                            // TODO: Navigate to PDF Viewer
                            // Intent to open PDF viewer with document.filePath
                        },
                        onAddClick = {
                            // TODO: Navigate to Import Flow
                            // Open file picker to select PDF
                        }
                    )
                }
            }
        }
    }
}
