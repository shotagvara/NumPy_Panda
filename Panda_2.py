import pandas as pd


# Load data
data = pd.read_excel("./data/task_2_data_ex.xlsx")


# Monthly -> annual BOM
result = data.groupby([
    "year",
    "plant_id",
    "produced_material",
    "produced_material_production_type",
    "produced_material_release_type",
    "component_material",
    "component_material_production_type",
    "component_material_release_type"
], dropna=False)[
    ["produced_material_quantity", "component_material_quantity"]
].sum().reset_index()


# Recursive BOM explosion
def explode(material, year, plant, fin_material):
    current = result.loc[
        (result["produced_material"] == material) &
        (result["year"] == year) &
        (result["plant_id"] == plant)
    ]

    rows = []

    for index, row in current.iterrows():
        # Keep original FIN
        row["fin_material_id"] = fin_material
        rows.append(row)

        # Continue only through PROD
        if row["component_material_release_type"] == "PROD":
            rows.extend(
                explode(
                    row["component_material"],
                    year,
                    plant,
                    fin_material
                )
            )

    return rows


# Select FIN materials
fin_rows = result.loc[
    result["produced_material_release_type"] == "FIN"
]


# Explode BOM for every FIN
all_rows = []

for index, row in fin_rows.iterrows():
    all_rows.extend(
        explode(
            row["component_material"],
            row["year"],
            row["plant_id"],
            row["produced_material"]
        )
    )

all_rows_df = pd.DataFrame(all_rows)


# Add original FIN information
final = all_rows_df.merge(
    fin_rows,
    left_on=[
        "fin_material_id",
        "year",
        "plant_id"
    ],
    right_on=[
        "produced_material",
        "year",
        "plant_id"
    ]
)


# Rename output columns
final = final.rename(columns={
    "produced_material_x": "prod_material_id",
    "produced_material_production_type_x": "prod_material_production_type",
    "produced_material_release_type_x": "prod_material_release_type",
    "produced_material_quantity_x": "prod_material_production_quantity",

    "component_material_x": "component_id",
    "component_material_production_type_x": "component_material_production_type",
    "component_material_release_type_x": "component_material_release_type",
    "component_material_quantity_x": "component_consumption_quantity",

    "produced_material_production_type_y": "fin_material_production_type",
    "produced_material_release_type_y": "fin_material_release_type",
    "produced_material_quantity_y": "fin_production_quantity",

    "plant_id": "plant"
})


# Final output structure
final = final[
    [
        "plant",
        "fin_material_id",
        "fin_material_release_type",
        "fin_material_production_type",
        "fin_production_quantity",
        "prod_material_id",
        "prod_material_release_type",
        "prod_material_production_type",
        "prod_material_production_quantity",
        "component_id",
        "component_material_release_type",
        "component_material_production_type",
        "component_consumption_quantity",
        "year"
    ]
]


print(final)