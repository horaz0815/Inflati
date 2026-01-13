package com.weiner.quotesapp.adapters

import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.ImageButton
import android.widget.TextView
import androidx.recyclerview.widget.RecyclerView
import com.weiner.quotesapp.R
import com.weiner.quotesapp.models.CleaningArea
import java.text.NumberFormat
import java.util.*

class CleaningAreaAdapter(
    private val areas: MutableList<CleaningArea>,
    private val onDeleteClick: (CleaningArea) -> Unit
) : RecyclerView.Adapter<CleaningAreaAdapter.ViewHolder>() {

    private val currencyFormat = NumberFormat.getCurrencyInstance(Locale.GERMANY)

    class ViewHolder(view: View) : RecyclerView.ViewHolder(view) {
        val txtAreaName: TextView = view.findViewById(R.id.txtAreaName)
        val txtAreaDetails: TextView = view.findViewById(R.id.txtAreaDetails)
        val txtMonthlyPrice: TextView = view.findViewById(R.id.txtMonthlyPrice)
        val btnDelete: ImageButton = view.findViewById(R.id.btnDelete)
    }

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): ViewHolder {
        val view = LayoutInflater.from(parent.context)
            .inflate(R.layout.item_cleaning_area, parent, false)
        return ViewHolder(view)
    }

    override fun onBindViewHolder(holder: ViewHolder, position: Int) {
        val area = areas[position]

        holder.txtAreaName.text = area.name
        holder.txtAreaDetails.text = "${area.areaType} • ${area.sizeInSqm} m² • ${area.frequency}"
        holder.txtMonthlyPrice.text = currencyFormat.format(area.calculateMonthlyPrice())

        holder.btnDelete.setOnClickListener {
            onDeleteClick(area)
        }
    }

    override fun getItemCount() = areas.size

    fun addArea(area: CleaningArea) {
        areas.add(area)
        notifyItemInserted(areas.size - 1)
    }

    fun removeArea(area: CleaningArea) {
        val position = areas.indexOf(area)
        if (position != -1) {
            areas.removeAt(position)
            notifyItemRemoved(position)
        }
    }

    fun getAreas(): List<CleaningArea> = areas.toList()
}
