package com.weiner.quotesapp.utils

import android.content.Context
import android.graphics.Canvas
import android.graphics.Color
import android.graphics.Paint
import android.graphics.Typeface
import android.graphics.pdf.PdfDocument
import com.weiner.quotesapp.models.Quote
import java.io.File
import java.io.FileOutputStream
import java.text.NumberFormat
import java.util.*

object PdfGenerator {

    private val currencyFormat = NumberFormat.getCurrencyInstance(Locale.GERMANY)
    private const val PAGE_WIDTH = 595
    private const val PAGE_HEIGHT = 842
    private const val MARGIN = 40f

    fun generateQuotePdf(context: Context, quote: Quote): File {
        val fileName = "Angebot_${quote.getQuoteNumber()}.pdf"
        val file = File(context.getExternalFilesDir(null), fileName)

        val pdfDocument = PdfDocument()
        val pageInfo = PdfDocument.PageInfo.Builder(PAGE_WIDTH, PAGE_HEIGHT, 1).create()
        val page = pdfDocument.startPage(pageInfo)
        val canvas = page.canvas

        var yPosition = MARGIN

        yPosition = drawCompanyHeader(canvas, yPosition)
        yPosition += 20f
        yPosition = drawQuoteInfo(canvas, yPosition, quote)
        yPosition += 20f
        yPosition = drawCustomerInfo(canvas, yPosition, quote)
        yPosition += 30f
        yPosition = drawTitle(canvas, yPosition)
        yPosition += 20f
        yPosition = drawItemsTable(canvas, yPosition, quote)
        yPosition += 20f
        yPosition = drawSummary(canvas, yPosition, quote)
        yPosition += 30f
        drawFooter(canvas, yPosition, quote)

        pdfDocument.finishPage(page)

        FileOutputStream(file).use { outputStream ->
            pdfDocument.writeTo(outputStream)
        }
        pdfDocument.close()

        return file
    }

    private fun drawCompanyHeader(canvas: Canvas, startY: Float): Float {
        var y = startY

        val titlePaint = Paint().apply {
            color = Color.rgb(25, 118, 210)
            textSize = 20f
            typeface = Typeface.create(Typeface.DEFAULT, Typeface.BOLD)
            isAntiAlias = true
        }

        val textPaint = Paint().apply {
            color = Color.DKGRAY
            textSize = 10f
            isAntiAlias = true
        }

        canvas.drawText("Weiner Gebäudeservice GmbH", MARGIN, y, titlePaint)
        y += 25f
        canvas.drawText("Musterstraße 123", MARGIN, y, textPaint)
        y += 15f
        canvas.drawText("12345 Musterstadt", MARGIN, y, textPaint)
        y += 15f
        canvas.drawText("Tel: +49 123 456789", MARGIN, y, textPaint)
        y += 15f
        canvas.drawText("E-Mail: info@weiner-gebaeudeservice.de", MARGIN, y, textPaint)
        y += 20f

        val linePaint = Paint().apply {
            color = Color.rgb(25, 118, 210)
            strokeWidth = 2f
        }
        canvas.drawLine(MARGIN, y, PAGE_WIDTH - MARGIN, y, linePaint)

        return y + 10f
    }

    private fun drawQuoteInfo(canvas: Canvas, startY: Float, quote: Quote): Float {
        var y = startY

        val boldPaint = Paint().apply {
            color = Color.BLACK
            textSize = 10f
            typeface = Typeface.create(Typeface.DEFAULT, Typeface.BOLD)
            isAntiAlias = true
        }

        val normalPaint = Paint().apply {
            color = Color.BLACK
            textSize = 10f
            isAntiAlias = true
        }

        canvas.drawText("Angebotsnummer:", MARGIN, y, boldPaint)
        y += 15f
        canvas.drawText(quote.getQuoteNumber(), MARGIN, y, normalPaint)
        y += 20f
        canvas.drawText("Datum: ${quote.getFormattedDate()}", MARGIN, y, normalPaint)
        y += 15f

        val italicPaint = Paint().apply {
            color = Color.DKGRAY
            textSize = 9f
            typeface = Typeface.create(Typeface.DEFAULT, Typeface.ITALIC)
            isAntiAlias = true
        }
        canvas.drawText("Gültig bis: ${quote.getFormattedValidUntilDate()}", MARGIN, y, italicPaint)

        return y + 10f
    }

    private fun drawCustomerInfo(canvas: Canvas, startY: Float, quote: Quote): Float {
        var y = startY

        val boldPaint = Paint().apply {
            color = Color.BLACK
            textSize = 11f
            typeface = Typeface.create(Typeface.DEFAULT, Typeface.BOLD)
            isAntiAlias = true
        }

        val normalPaint = Paint().apply {
            color = Color.BLACK
            textSize = 10f
            isAntiAlias = true
        }

        canvas.drawText("Kunde:", MARGIN, y, boldPaint)
        y += 20f
        canvas.drawText(quote.customer.name, MARGIN, y, normalPaint)
        y += 15f
        canvas.drawText(quote.customer.address, MARGIN, y, normalPaint)
        y += 15f
        canvas.drawText(quote.customer.city, MARGIN, y, normalPaint)
        y += 15f
        canvas.drawText("E-Mail: ${quote.customer.email}", MARGIN, y, normalPaint)
        y += 15f
        canvas.drawText("Tel: ${quote.customer.phone}", MARGIN, y, normalPaint)

        return y + 10f
    }

    private fun drawTitle(canvas: Canvas, startY: Float): Float {
        val titlePaint = Paint().apply {
            color = Color.rgb(25, 118, 210)
            textSize = 16f
            typeface = Typeface.create(Typeface.DEFAULT, Typeface.BOLD)
            isAntiAlias = true
        }

        canvas.drawText("Angebot für Reinigungsleistungen", MARGIN, startY, titlePaint)
        return startY + 10f
    }

    private fun drawItemsTable(canvas: Canvas, startY: Float, quote: Quote): Float {
        var y = startY

        val headerPaint = Paint().apply {
            color = Color.WHITE
            textSize = 9f
            typeface = Typeface.create(Typeface.DEFAULT, Typeface.BOLD)
            isAntiAlias = true
        }

        val headerBgPaint = Paint().apply {
            color = Color.rgb(25, 118, 210)
            style = Paint.Style.FILL
        }

        val textPaint = Paint().apply {
            color = Color.BLACK
            textSize = 9f
            isAntiAlias = true
        }

        val cellPaint = Paint().apply {
            color = Color.rgb(245, 245, 245)
            style = Paint.Style.FILL
        }

        val borderPaint = Paint().apply {
            color = Color.LTGRAY
            strokeWidth = 1f
        }

        val rowHeight = 25f
        canvas.drawRect(MARGIN, y, PAGE_WIDTH - MARGIN, y + rowHeight, headerBgPaint)

        canvas.drawText("Bereich", MARGIN + 5f, y + 17f, headerPaint)
        canvas.drawText("Art / Fläche", MARGIN + 150f, y + 17f, headerPaint)
        canvas.drawText("Häufigkeit", MARGIN + 280f, y + 17f, headerPaint)
        canvas.drawText("Preis/m²", MARGIN + 370f, y + 17f, headerPaint)
        canvas.drawText("Monatlich", MARGIN + 450f, y + 17f, headerPaint)

        y += rowHeight

        quote.areas.forEachIndexed { index, area ->
            if (index % 2 == 0) {
                canvas.drawRect(MARGIN, y, PAGE_WIDTH - MARGIN, y + rowHeight * 1.5f, cellPaint)
            }

            canvas.drawText(area.name, MARGIN + 5f, y + 15f, textPaint)
            canvas.drawText(area.areaType, MARGIN + 150f, y + 15f, textPaint)
            canvas.drawText("${area.sizeInSqm} m²", MARGIN + 150f, y + 27f, textPaint)
            canvas.drawText(area.frequency, MARGIN + 280f, y + 15f, textPaint)
            canvas.drawText(currencyFormat.format(area.pricePerSqm), MARGIN + 370f, y + 15f, textPaint)

            val boldTextPaint = Paint().apply {
                color = Color.BLACK
                textSize = 9f
                typeface = Typeface.create(Typeface.DEFAULT, Typeface.BOLD)
                isAntiAlias = true
            }
            canvas.drawText(currencyFormat.format(area.calculateMonthlyPrice()), MARGIN + 450f, y + 15f, boldTextPaint)

            y += rowHeight * 1.5f
            canvas.drawLine(MARGIN, y, PAGE_WIDTH - MARGIN, y, borderPaint)
        }

        return y + 10f
    }

    private fun drawSummary(canvas: Canvas, startY: Float, quote: Quote): Float {
        var y = startY

        val labelPaint = Paint().apply {
            color = Color.BLACK
            textSize = 11f
            typeface = Typeface.create(Typeface.DEFAULT, Typeface.BOLD)
            isAntiAlias = true
        }

        val valuePaint = Paint().apply {
            color = Color.rgb(25, 118, 210)
            textSize = 14f
            typeface = Typeface.create(Typeface.DEFAULT, Typeface.BOLD)
            isAntiAlias = true
        }

        val smallLabelPaint = Paint().apply {
            color = Color.BLACK
            textSize = 10f
            isAntiAlias = true
        }

        val smallValuePaint = Paint().apply {
            color = Color.BLACK
            textSize = 11f
            typeface = Typeface.create(Typeface.DEFAULT, Typeface.BOLD)
            isAntiAlias = true
        }

        canvas.drawText("Monatlicher Gesamtpreis (netto)", MARGIN + 200f, y, labelPaint)
        canvas.drawText(currencyFormat.format(quote.calculateMonthlyTotal()), MARGIN + 450f, y, valuePaint)
        y += 25f

        canvas.drawText("Jährlicher Gesamtpreis (netto)", MARGIN + 200f, y, smallLabelPaint)
        canvas.drawText(currencyFormat.format(quote.calculateYearlyTotal()), MARGIN + 450f, y, smallValuePaint)
        y += 20f

        val notePaint = Paint().apply {
            color = Color.DKGRAY
            textSize = 9f
            typeface = Typeface.create(Typeface.DEFAULT, Typeface.ITALIC)
            isAntiAlias = true
        }
        canvas.drawText("zzgl. gesetzlicher Mehrwertsteuer", MARGIN + 200f, y, notePaint)

        return y + 10f
    }

    private fun drawFooter(canvas: Canvas, startY: Float, quote: Quote) {
        var y = startY + 20f

        val textPaint = Paint().apply {
            color = Color.DKGRAY
            textSize = 8f
            isAntiAlias = true
        }

        val boldPaint = Paint().apply {
            color = Color.BLACK
            textSize = 10f
            typeface = Typeface.create(Typeface.DEFAULT, Typeface.BOLD)
            isAntiAlias = true
        }

        canvas.drawText("Allgemeine Hinweise:", MARGIN, y, boldPaint)
        y += 15f

        val notes = listOf(
            "• Alle Preise verstehen sich als Nettopreise zzgl. der gesetzlichen Mehrwertsteuer",
            "• Die Reinigung erfolgt außerhalb der regulären Geschäftszeiten",
            "• Reinigungsmaterial und -geräte werden von uns gestellt",
            "• Vertragslaufzeit: 24 Monate mit 3-monatiger Kündigungsfrist",
            "• Dieses Angebot ist gültig bis ${quote.getFormattedValidUntilDate()}"
        )

        notes.forEach { note ->
            canvas.drawText(note, MARGIN, y, textPaint)
            y += 12f
        }

        y += 15f

        canvas.drawText("Wir freuen uns auf eine erfolgreiche Zusammenarbeit!", MARGIN, y, boldPaint)
        y += 20f
        canvas.drawText("Mit freundlichen Grüßen", MARGIN, y, textPaint)
        y += 15f
        canvas.drawText("Weiner Gebäudeservice GmbH", MARGIN, y, textPaint)
    }
}
