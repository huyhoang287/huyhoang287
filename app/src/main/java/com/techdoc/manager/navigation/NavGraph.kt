package com.techdoc.manager.navigation

import androidx.compose.runtime.*
import androidx.compose.ui.platform.LocalContext
import androidx.lifecycle.viewmodel.compose.viewModel
import androidx.navigation.NavHostController
import androidx.navigation.NavType
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import androidx.navigation.navArgument
import com.techdoc.manager.ui.components.AddDocumentDialog
import com.techdoc.manager.ui.screens.home.HomeScreen
import com.techdoc.manager.ui.screens.pdfviewer.PdfViewerScreen
import com.techdoc.manager.viewmodel.HomeViewModel

/**
 * NavGraph chính của ứng dụng
 * Quản lý điều hướng giữa các màn hình
 */
@Composable
fun TechDocNavGraph(
    navController: NavHostController,
    homeViewModel: HomeViewModel = viewModel()
) {
    var showAddDialog by remember { mutableStateOf(false) }

    // Add Document Dialog
    if (showAddDialog) {
        AddDocumentDialog(
            onDismiss = { showAddDialog = false },
            onConfirm = { uri, title, code, category, tags ->
                homeViewModel.importDocument(uri, title, code, category, tags)
                showAddDialog = false
            }
        )
    }

    NavHost(
        navController = navController,
        startDestination = NavRoutes.Home.route
    ) {
        // Home Screen
        composable(NavRoutes.Home.route) {
            HomeScreen(
                viewModel = homeViewModel,
                onDocumentClick = { document ->
                    navController.navigate(
                        NavRoutes.PdfViewer.createRoute(
                            filePath = document.filePath,
                            title = document.title
                        )
                    )
                },
                onAddClick = {
                    showAddDialog = true
                }
            )
        }

        // PDF Viewer Screen
        composable(
            route = NavRoutes.PdfViewer.route,
            arguments = listOf(
                navArgument("filePath") { type = NavType.StringType },
                navArgument("title") { type = NavType.StringType }
            )
        ) { backStackEntry ->
            val encodedFilePath = backStackEntry.arguments?.getString("filePath") ?: ""
            val encodedTitle = backStackEntry.arguments?.getString("title") ?: ""

            val filePath = NavRoutes.PdfViewer.decodeFilePath(encodedFilePath)
            val title = NavRoutes.PdfViewer.decodeTitle(encodedTitle)

            PdfViewerScreen(
                filePath = filePath,
                documentTitle = title,
                onNavigateBack = {
                    navController.popBackStack()
                }
            )
        }
    }
}
