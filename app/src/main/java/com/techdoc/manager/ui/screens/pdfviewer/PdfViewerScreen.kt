package com.techdoc.manager.ui.screens.pdfviewer

import android.graphics.Bitmap
import android.graphics.pdf.PdfRenderer
import android.os.ParcelFileDescriptor
import androidx.compose.foundation.Image
import androidx.compose.foundation.background
import androidx.compose.foundation.gestures.detectTransformGestures
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.itemsIndexed
import androidx.compose.foundation.lazy.rememberLazyListState
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material.icons.filled.ZoomIn
import androidx.compose.material.icons.filled.ZoomOut
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.asImageBitmap
import androidx.compose.ui.graphics.graphicsLayer
import androidx.compose.ui.input.pointer.pointerInput
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.platform.LocalDensity
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import java.io.File

/**
 * Màn hình xem PDF với khả năng zoom và cuộn mượt
 * Sử dụng Android PdfRenderer native API
 */
@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun PdfViewerScreen(
    filePath: String,
    documentTitle: String,
    onNavigateBack: () -> Unit
) {
    val context = LocalContext.current
    var pdfRenderer by remember { mutableStateOf<PdfRenderer?>(null) }
    var pageCount by remember { mutableIntStateOf(0) }
    var currentPage by remember { mutableIntStateOf(0) }
    var isLoading by remember { mutableStateOf(true) }
    var errorMessage by remember { mutableStateOf<String?>(null) }
    var scale by remember { mutableFloatStateOf(1f) }

    val listState = rememberLazyListState()

    // Load PDF file
    LaunchedEffect(filePath) {
        withContext(Dispatchers.IO) {
            try {
                val file = File(filePath)
                if (file.exists()) {
                    val fileDescriptor = ParcelFileDescriptor.open(
                        file,
                        ParcelFileDescriptor.MODE_READ_ONLY
                    )
                    pdfRenderer = PdfRenderer(fileDescriptor)
                    pageCount = pdfRenderer?.pageCount ?: 0
                    isLoading = false
                } else {
                    errorMessage = "File không tồn tại"
                    isLoading = false
                }
            } catch (e: Exception) {
                errorMessage = "Không thể mở file PDF: ${e.message}"
                isLoading = false
            }
        }
    }

    // Cleanup
    DisposableEffect(Unit) {
        onDispose {
            pdfRenderer?.close()
        }
    }

    // Track current page based on scroll position
    LaunchedEffect(listState.firstVisibleItemIndex) {
        currentPage = listState.firstVisibleItemIndex
    }

    Scaffold(
        topBar = {
            TopAppBar(
                title = {
                    Column {
                        Text(
                            text = documentTitle,
                            maxLines = 1,
                            overflow = TextOverflow.Ellipsis,
                            style = MaterialTheme.typography.titleMedium,
                            fontWeight = FontWeight.Bold
                        )
                        if (pageCount > 0) {
                            Text(
                                text = "Trang ${currentPage + 1} / $pageCount",
                                style = MaterialTheme.typography.bodySmall,
                                color = MaterialTheme.colorScheme.onSurfaceVariant
                            )
                        }
                    }
                },
                navigationIcon = {
                    IconButton(onClick = onNavigateBack) {
                        Icon(
                            imageVector = Icons.AutoMirrored.Filled.ArrowBack,
                            contentDescription = "Quay lại"
                        )
                    }
                },
                actions = {
                    // Zoom controls
                    IconButton(
                        onClick = { scale = (scale - 0.25f).coerceAtLeast(0.5f) }
                    ) {
                        Icon(
                            imageVector = Icons.Default.ZoomOut,
                            contentDescription = "Thu nhỏ"
                        )
                    }
                    Text(
                        text = "${(scale * 100).toInt()}%",
                        style = MaterialTheme.typography.bodySmall
                    )
                    IconButton(
                        onClick = { scale = (scale + 0.25f).coerceAtMost(3f) }
                    ) {
                        Icon(
                            imageVector = Icons.Default.ZoomIn,
                            contentDescription = "Phóng to"
                        )
                    }
                },
                colors = TopAppBarDefaults.topAppBarColors(
                    containerColor = MaterialTheme.colorScheme.surface
                )
            )
        }
    ) { paddingValues ->
        Box(
            modifier = Modifier
                .fillMaxSize()
                .padding(paddingValues)
                .background(MaterialTheme.colorScheme.surfaceVariant)
        ) {
            when {
                isLoading -> {
                    CircularProgressIndicator(
                        modifier = Modifier.align(Alignment.Center)
                    )
                }
                errorMessage != null -> {
                    Column(
                        modifier = Modifier
                            .align(Alignment.Center)
                            .padding(32.dp),
                        horizontalAlignment = Alignment.CenterHorizontally
                    ) {
                        Text(
                            text = "Lỗi",
                            style = MaterialTheme.typography.headlineSmall,
                            color = MaterialTheme.colorScheme.error
                        )
                        Spacer(modifier = Modifier.height(8.dp))
                        Text(
                            text = errorMessage!!,
                            style = MaterialTheme.typography.bodyMedium,
                            color = MaterialTheme.colorScheme.onSurfaceVariant
                        )
                        Spacer(modifier = Modifier.height(16.dp))
                        Button(onClick = onNavigateBack) {
                            Text("Quay lại")
                        }
                    }
                }
                pdfRenderer != null -> {
                    PdfPagesList(
                        pdfRenderer = pdfRenderer!!,
                        pageCount = pageCount,
                        scale = scale,
                        listState = listState,
                        onScaleChange = { newScale -> scale = newScale }
                    )
                }
            }
        }
    }
}

/**
 * Hiển thị danh sách các trang PDF với LazyColumn
 */
@Composable
fun PdfPagesList(
    pdfRenderer: PdfRenderer,
    pageCount: Int,
    scale: Float,
    listState: androidx.compose.foundation.lazy.LazyListState,
    onScaleChange: (Float) -> Unit
) {
    var offsetX by remember { mutableFloatStateOf(0f) }
    var offsetY by remember { mutableFloatStateOf(0f) }

    LazyColumn(
        state = listState,
        modifier = Modifier
            .fillMaxSize()
            .pointerInput(Unit) {
                detectTransformGestures { _, pan, zoom, _ ->
                    val newScale = (scale * zoom).coerceIn(0.5f, 3f)
                    onScaleChange(newScale)

                    if (newScale > 1f) {
                        offsetX += pan.x
                        offsetY += pan.y
                    } else {
                        offsetX = 0f
                        offsetY = 0f
                    }
                }
            },
        contentPadding = PaddingValues(8.dp),
        verticalArrangement = Arrangement.spacedBy(8.dp)
    ) {
        itemsIndexed(
            items = (0 until pageCount).toList(),
            key = { index, _ -> index }
        ) { index, _ ->
            PdfPageItem(
                pdfRenderer = pdfRenderer,
                pageIndex = index,
                scale = scale,
                offsetX = offsetX,
                offsetY = offsetY
            )
        }
    }
}

/**
 * Hiển thị một trang PDF
 */
@Composable
fun PdfPageItem(
    pdfRenderer: PdfRenderer,
    pageIndex: Int,
    scale: Float,
    offsetX: Float,
    offsetY: Float
) {
    val density = LocalDensity.current
    var bitmap by remember { mutableStateOf<Bitmap?>(null) }
    var isPageLoading by remember { mutableStateOf(true) }

    LaunchedEffect(pageIndex, scale) {
        withContext(Dispatchers.IO) {
            try {
                isPageLoading = true
                val page = pdfRenderer.openPage(pageIndex)

                // Calculate dimensions based on scale
                val baseWidth = with(density) { 400.dp.toPx().toInt() }
                val aspectRatio = page.height.toFloat() / page.width.toFloat()
                val scaledWidth = (baseWidth * scale).toInt()
                val scaledHeight = (scaledWidth * aspectRatio).toInt()

                val newBitmap = Bitmap.createBitmap(
                    scaledWidth,
                    scaledHeight,
                    Bitmap.Config.ARGB_8888
                )

                page.render(
                    newBitmap,
                    null,
                    null,
                    PdfRenderer.Page.RENDER_MODE_FOR_DISPLAY
                )
                page.close()

                bitmap = newBitmap
                isPageLoading = false
            } catch (e: Exception) {
                isPageLoading = false
            }
        }
    }

    Card(
        modifier = Modifier.fillMaxWidth(),
        colors = CardDefaults.cardColors(
            containerColor = MaterialTheme.colorScheme.surface
        ),
        elevation = CardDefaults.cardElevation(defaultElevation = 2.dp)
    ) {
        Box(
            modifier = Modifier
                .fillMaxWidth()
                .aspectRatio(1f / 1.414f) // A4 ratio
                .graphicsLayer {
                    if (scale > 1f) {
                        translationX = offsetX
                        translationY = offsetY
                    }
                },
            contentAlignment = Alignment.Center
        ) {
            if (isPageLoading) {
                CircularProgressIndicator(
                    modifier = Modifier.size(32.dp)
                )
            } else {
                bitmap?.let { bmp ->
                    Image(
                        bitmap = bmp.asImageBitmap(),
                        contentDescription = "Trang ${pageIndex + 1}",
                        modifier = Modifier.fillMaxSize(),
                        contentScale = ContentScale.Fit
                    )
                }
            }
        }
    }
}
