package com.techdoc.manager.navigation

import java.net.URLDecoder
import java.net.URLEncoder
import java.nio.charset.StandardCharsets

/**
 * Định nghĩa các route navigation trong app
 */
sealed class NavRoutes(val route: String) {

    /**
     * Màn hình Home - Danh sách tài liệu
     */
    object Home : NavRoutes("home")

    /**
     * Màn hình PDF Viewer
     * Arguments: filePath, title
     */
    object PdfViewer : NavRoutes("pdf_viewer/{filePath}/{title}") {
        fun createRoute(filePath: String, title: String): String {
            val encodedPath = URLEncoder.encode(filePath, StandardCharsets.UTF_8.toString())
            val encodedTitle = URLEncoder.encode(title, StandardCharsets.UTF_8.toString())
            return "pdf_viewer/$encodedPath/$encodedTitle"
        }

        fun decodeFilePath(encodedPath: String): String {
            return URLDecoder.decode(encodedPath, StandardCharsets.UTF_8.toString())
        }

        fun decodeTitle(encodedTitle: String): String {
            return URLDecoder.decode(encodedTitle, StandardCharsets.UTF_8.toString())
        }
    }
}
