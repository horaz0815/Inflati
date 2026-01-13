package com.weiner.quotesapp.utils

import android.content.Context
import com.itextpdf.kernel.colors.ColorConstants
import com.itextpdf.kernel.colors.DeviceRgb
import com.itextpdf.kernel.geom.PageSize
import com.itextpdf.kernel.pdf.PdfDocument
import com.itextpdf.kernel.pdf.PdfWriter
import com.itextpdf.layout.Document
import com.itextpdf.layout.borders.Border
import com.itextpdf.layout.borders.SolidBorder
import com.itextpdf.layout.element.Cell
import com.itextpdf.layout.element.Paragraph
import com.itextpdf.layout.element.Table
import com.itextpdf.layout.property.TextAlignment
import com.itextpdf.layout.property.UnitValue
import com.weiner.quotesapp.models.Quote
import java.io.File
import java.text.NumberFormat
import java.util.*

object PdfGenerator {

    private val currencyFormat = NumberFormat.getCurrencyInstance(Locale.GERMANY)
    private val primaryColor = DeviceRgb(25, 118, 210) // Blue
    private val lightGrayColor = DeviceRgb(245, 245, 245)

    fun generateQuotePdf(context: Context, quote: Quote): File {
        val fileName = "Angebot_${quote.getQuoteNumber()}.pdf"
        val file = File(context.getExternalFilesDir(null), fileName)

        val pdfWriter = PdfWriter(file)
        val pdfDocument = PdfDocument(pdfWriter)
        val document = Document(pdfDocument, PageSize.A4)
        document.setMargins(40f, 40f, 40f, 40f)

        // Header - Company Info
        addCompanyHeader(document)

        // Quote Number and Date
        addQuoteInfo(document, quote)

        // Customer Info
        addCustomerInfo(document, quote)

        // Spacing
        document.add(Paragraph("\n"))

        // Quote Title
        val title = Paragraph("Angebot für Reinigungsleistungen")
            .setFontSize(16f)
            .setBold()
            .setFontColor(primaryColor)
        document.add(title)

        document.add(Paragraph("\n"))

        // Items Table
        addItemsTable(document, quote)

        // Spacing
        document.add(Paragraph("\n"))

        // Summary
        addSummary(document, quote)

        // Footer
        addFooter(document, quote)

        document.close()
        return file
    }

    private fun addCompanyHeader(document: Document) {
        val companyName = Paragraph("Weiner Gebäudeservice GmbH")
            .setFontSize(20f)
            .setBold()
            .setFontColor(primaryColor)

        val companyInfo = Paragraph(
            "Musterstraße 123\n" +
                    "12345 Musterstadt\n" +
                    "Tel: +49 123 456789\n" +
                    "E-Mail: info@weiner-gebaeudeservice.de"
        )
            .setFontSize(10f)
            .setFontColor(ColorConstants.DARK_GRAY)

        document.add(companyName)
        document.add(companyInfo)

        // Separator line
        val separator = Paragraph("\n")
            .setBorderBottom(SolidBorder(primaryColor, 2f))
        document.add(separator)
    }

    private fun addQuoteInfo(document: Document, quote: Quote) {
        val table = Table(UnitValue.createPercentArray(floatArrayOf(1f, 1f)))
            .useAllAvailableWidth()

        val quoteNumber = Paragraph("Angebotsnummer:\n${quote.getQuoteNumber()}")
            .setFontSize(10f)
            .setBold()

        val date = Paragraph("Datum:\n${quote.getFormattedDate()}")
            .setFontSize(10f)
            .setTextAlignment(TextAlignment.RIGHT)

        table.addCell(Cell().add(quoteNumber).setBorder(Border.NO_BORDER))
        table.addCell(Cell().add(date).setBorder(Border.NO_BORDER))

        document.add(table)

        val validUntil = Paragraph("Gültig bis: ${quote.getFormattedValidUntilDate()}")
            .setFontSize(9f)
            .setFontColor(ColorConstants.DARK_GRAY)
            .setItalic()
        document.add(validUntil)
    }

    private fun addCustomerInfo(document: Document, quote: Quote) {
        document.add(Paragraph("\n"))

        val customerTitle = Paragraph("Kunde:")
            .setFontSize(11f)
            .setBold()

        val customerInfo = Paragraph(
            "${quote.customer.name}\n" +
                    "${quote.customer.address}\n" +
                    "${quote.customer.city}\n" +
                    "E-Mail: ${quote.customer.email}\n" +
                    "Tel: ${quote.customer.phone}"
        )
            .setFontSize(10f)

        document.add(customerTitle)
        document.add(customerInfo)
    }

    private fun addItemsTable(document: Document, quote: Quote) {
        val table = Table(UnitValue.createPercentArray(floatArrayOf(3f, 2f, 1.5f, 1.5f, 2f)))
            .useAllAvailableWidth()

        // Header
        val headers = listOf("Bereich", "Art / Fläche", "Häufigkeit", "Preis/m²", "Monatlich")
        headers.forEach { header ->
            table.addHeaderCell(
                Cell()
                    .add(Paragraph(header).setBold().setFontColor(ColorConstants.WHITE))
                    .setBackgroundColor(primaryColor)
                    .setTextAlignment(TextAlignment.CENTER)
                    .setPadding(8f)
            )
        }

        // Items
        quote.areas.forEachIndexed { index, area ->
            val backgroundColor = if (index % 2 == 0) ColorConstants.WHITE else lightGrayColor

            table.addCell(
                Cell()
                    .add(Paragraph(area.name).setFontSize(10f))
                    .setBackgroundColor(backgroundColor)
                    .setPadding(8f)
            )

            table.addCell(
                Cell()
                    .add(Paragraph("${area.areaType}\n${area.sizeInSqm} m²").setFontSize(9f))
                    .setBackgroundColor(backgroundColor)
                    .setPadding(8f)
            )

            table.addCell(
                Cell()
                    .add(Paragraph(area.frequency).setFontSize(9f))
                    .setBackgroundColor(backgroundColor)
                    .setTextAlignment(TextAlignment.CENTER)
                    .setPadding(8f)
            )

            table.addCell(
                Cell()
                    .add(Paragraph(currencyFormat.format(area.pricePerSqm)).setFontSize(9f))
                    .setBackgroundColor(backgroundColor)
                    .setTextAlignment(TextAlignment.RIGHT)
                    .setPadding(8f)
            )

            table.addCell(
                Cell()
                    .add(Paragraph(currencyFormat.format(area.calculateMonthlyPrice())).setFontSize(9f).setBold())
                    .setBackgroundColor(backgroundColor)
                    .setTextAlignment(TextAlignment.RIGHT)
                    .setPadding(8f)
            )
        }

        document.add(table)
    }

    private fun addSummary(document: Document, quote: Quote) {
        val summaryTable = Table(UnitValue.createPercentArray(floatArrayOf(3f, 2f)))
            .useAllAvailableWidth()

        // Monthly Total
        summaryTable.addCell(
            Cell()
                .add(Paragraph("Monatlicher Gesamtpreis (netto)").setBold().setFontSize(11f))
                .setBorder(Border.NO_BORDER)
                .setTextAlignment(TextAlignment.RIGHT)
                .setPadding(5f)
        )

        summaryTable.addCell(
            Cell()
                .add(
                    Paragraph(currencyFormat.format(quote.calculateMonthlyTotal()))
                        .setBold()
                        .setFontSize(14f)
                        .setFontColor(primaryColor)
                )
                .setBorder(Border.NO_BORDER)
                .setTextAlignment(TextAlignment.RIGHT)
                .setPadding(5f)
        )

        // Yearly Total
        summaryTable.addCell(
            Cell()
                .add(Paragraph("Jährlicher Gesamtpreis (netto)").setFontSize(10f))
                .setBorder(Border.NO_BORDER)
                .setTextAlignment(TextAlignment.RIGHT)
                .setPadding(5f)
        )

        summaryTable.addCell(
            Cell()
                .add(Paragraph(currencyFormat.format(quote.calculateYearlyTotal())).setFontSize(11f))
                .setBorder(Border.NO_BORDER)
                .setTextAlignment(TextAlignment.RIGHT)
                .setPadding(5f)
        )

        document.add(summaryTable)

        // VAT Note
        val vatNote = Paragraph("zzgl. gesetzlicher Mehrwertsteuer")
            .setFontSize(9f)
            .setFontColor(ColorConstants.DARK_GRAY)
            .setTextAlignment(TextAlignment.RIGHT)
            .setItalic()
        document.add(vatNote)
    }

    private fun addFooter(document: Document, quote: Quote) {
        document.add(Paragraph("\n\n"))

        val terms = Paragraph(
            "Allgemeine Hinweise:\n" +
                    "• Alle Preise verstehen sich als Nettopreise zzgl. der gesetzlichen Mehrwertsteuer\n" +
                    "• Die Reinigung erfolgt außerhalb der regulären Geschäftszeiten\n" +
                    "• Reinigungsmaterial und -geräte werden von uns gestellt\n" +
                    "• Vertragslaufzeit: 24 Monate mit 3-monatiger Kündigungsfrist\n" +
                    "• Dieses Angebot ist gültig bis ${quote.getFormattedValidUntilDate()}"
        )
            .setFontSize(8f)
            .setFontColor(ColorConstants.DARK_GRAY)

        document.add(terms)

        document.add(Paragraph("\n"))

        val closing = Paragraph(
            "Wir freuen uns auf eine erfolgreiche Zusammenarbeit!\n\n" +
                    "Mit freundlichen Grüßen\n" +
                    "Weiner Gebäudeservice GmbH"
        )
            .setFontSize(10f)

        document.add(closing)
    }
}
