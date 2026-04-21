import bentoml
import pandas as pd
import numpy as np
from schemas import BuildingInput

@bentoml.service()
class EnergyPrediction:
    #Le mapping pour le regroupement en classe
    mapping_usage = {
    # Bureau / Finance
    'Office'                                              : 'Bureau_Finance',
    'Financial Office'                                    : 'Bureau_Finance',
    'Bank Branch'                                         : 'Bureau_Finance',

    # Logistique / Stockage
    'Non-Refrigerated Warehouse'                          : 'Logistique_Stockage',
    'Distribution Center'                                 : 'Logistique_Stockage',
    'Parking'                                             : 'Logistique_Stockage',
    'Self-Storage Facility'                               : 'Logistique_Stockage',
    'Refrigerated Warehouse'                              : 'Logistique_Stockage',

    # Commerce / Retail
    'Retail Store'                                        : 'Commerce_Retail',
    'Strip Mall'                                          : 'Commerce_Retail',
    'Automobile Dealership'                               : 'Commerce_Retail',
    'Repair Services (Vehicle, Shoe, Locksmith, etc)'     : 'Commerce_Retail',
    'Other - Mall'                                        : 'Commerce_Retail',
    'Other - Services'                                    : 'Commerce_Retail',
    'Lifestyle Center'                                    : 'Commerce_Retail',
    'Personal Services (Health/Beauty, Dry Cleaning, etc)': 'Commerce_Retail',
    'Wholesale Club/Supercenter'                          : 'Commerce_Retail',
    'Enclosed Mall'                                       : 'Commerce_Retail',

    # Hôtellerie / Logement
    'Hotel'                                               : 'Hotellerie_Logement',
    'Residence Hall/Dormitory'                            : 'Hotellerie_Logement',
    'Multifamily Housing'                                 : 'Hotellerie_Logement',
    'Other - Lodging/Residential'                         : 'Hotellerie_Logement',

    # Éducation
    'K-12 School'                                         : 'Education',
    'College/University'                                  : 'Education',
    'Other - Education'                                   : 'Education',
    'Adult Education'                                     : 'Education',
    'Pre-school/Daycare'                                  : 'Education',
    'Vocational School'                                   : 'Education',

    # Culture / Loisirs / Culte
    'Worship Facility'                                    : 'Culture_Loisirs_Culte',
    'Other - Recreation'                                  : 'Culture_Loisirs_Culte',
    'Other - Entertainment/Public Assembly'               : 'Culture_Loisirs_Culte',
    'Social/Meeting Hall'                                 : 'Culture_Loisirs_Culte',
    'Fitness Center/Health Club/Gym'                      : 'Culture_Loisirs_Culte',
    'Museum'                                              : 'Culture_Loisirs_Culte',
    'Performing Arts'                                     : 'Culture_Loisirs_Culte',
    'Movie Theater'                                       : 'Culture_Loisirs_Culte',
    'Swimming Pool'                                       : 'Culture_Loisirs_Culte',

    # Santé
    'Medical Office'                                      : 'Sante',
    'Senior Care Community'                               : 'Sante',
    'Hospital (General Medical & Surgical)'               : 'Sante',
    'Laboratory'                                          : 'Sante',
    'Other/Specialty Hospital'                            : 'Sante',
    'Urgent Care/Clinic/Other Outpatient'                 : 'Sante',
    'Residential Care Facility'                           : 'Sante',

    # Commerce alimentaire
    'Supermarket/Grocery Store'                           : 'Commerce_Alimentaire',
    'Restaurant'                                          : 'Commerce_Alimentaire',
    'Other - Restaurant/Bar'                              : 'Commerce_Alimentaire',
    'Food Service'                                        : 'Commerce_Alimentaire',
    'Bar/Nightclub'                                       : 'Commerce_Alimentaire',
    'Food Sales'                                          : 'Commerce_Alimentaire',
    'Convenience Store without Gas Station'               : 'Commerce_Alimentaire',
    'Fast Food Restaurant'                                : 'Commerce_Alimentaire',

    # Services publics / Industrie
    'Manufacturing/Industrial Plant'                      : 'Services_Publics_Industrie',
    'Data Center'                                         : 'Services_Publics_Industrie',
    'Prison/Incarceration'                                : 'Services_Publics_Industrie',
    'Other - Public Services'                             : 'Services_Publics_Industrie',
    'Other - Utility'                                     : 'Services_Publics_Industrie',
    'Police Station'                                      : 'Services_Publics_Industrie',
    'Courthouse'                                          : 'Services_Publics_Industrie',
    'Fire Station'                                        : 'Services_Publics_Industrie',
    'Other - Technology/Science'                          : 'Services_Publics_Industrie',
    'Library'                                             : 'Services_Publics_Industrie',

    # Autre
    'Other'                                               : 'Autre',
    }
    
    def __init__(self):
        # Chargement unique des objets au démarrage
        #model_ref = bentoml.models.get("grid_xgb_regressor:latest")
        self.model_ref = bentoml.models.get("grid_xgb_regressor:latest")
        self.scaler = self.model_ref.custom_objects["scaler"]
        self.feature_names = self.model_ref.custom_objects["feature_names"]
        self.regressor = bentoml.xgboost.load_model(self.model_ref)

    @bentoml.api
    def predict(self, data: BuildingInput) -> dict:
        # 1. On convertit l'objet validé Pydantic en DataFrame en reprenant les feature_names comme paramètres
        input_df = pd.DataFrame(0, index=[0], columns=self.feature_names)

        # 2. Règle : Building Age
        input_df['BuildingAge'] = 2026 - data.YearBuilt
        
        # 3. Règle : Énergies (conversion booléen vers int)
        input_df['Has_Steam'] = int(data.Has_Steam)
        input_df['Has_Gas'] = int(data.Has_Gas)
        input_df['Has_Electricity'] = int(data.Has_Electricity)

        # 4. Variables physiques
        input_df['NumberofBuildings'] = data.NumberofBuildings
        input_df['NumberofFloors'] = data.NumberofFloors
        input_df['PropertyGFAParking'] = data.PropertyGFAParking
        input_df['PropertyGFABuilding(s)'] = data.PropertyGFABuilding_s

        # 5. Règle : Mapping des 3 Usages (Ta boucle for adaptée à l'objet Pydantic)
        usages = [
            (data.LargestPropertyUseType, data.LargestPropertyUseTypeGFA),
            (data.SecondLargestPropertyUseType, data.SecondLargestPropertyUseTypeGFA),
            (data.ThirdLargestPropertyUseType, data.ThirdLargestPropertyUseTypeGFA)
        ]

        #Ce bloc de code ne sera executé que si les champs LargestPropertyUseType, SecondLargestPropertyUseType et ThirdLargestPropertyUseType sont renseignés
        #Chacun de ces champs deviendra tout à tour usage_enum grâce à la structure en triplet defini ci-dessus et la colonne 'usage'+'GFA' deviendra surface
        #Si cette colonne n'est pas supérieure à 0, alors là aussi, rien ne sera renseignée dans les nouvelles colonnes prévues à cet effet
        for usage_enum, surface in usages:
            if usage_enum and surface > 0:
                # On récupère la chaîne de caractères avec .value
                usage_name = usage_enum.value 
                category = self.mapping_usage.get(usage_name, 'Autre')
                col_name = f'GFA_{category}'
                if col_name in input_df.columns:
                    input_df[col_name] += surface
        '''
        for usage_name, surface in usages:
            if usage_name and surface > 0:
                category = self.mapping_usage.get(usage_name, 'Autre')
                col_name = f'GFA_{category}'
                if col_name in input_df.columns:
                    input_df[col_name] += surface
        '''
        # 6. Règle : Neighborhood (One Hot)
        col_nbhd = f'Nbhd_{data.Neighborhood.value}'
        if col_nbhd in input_df.columns:
            input_df[col_nbhd] = 1
        
        # 7. On applique le scaling (très important !) : En effet notre modèle s'applique sur des données scalés !
        input_df_scaled = self.scaler.transform(input_df)
        
        # 8. Prédiction normalisées(en log)
        log_pred = self.regressor.predict(input_df_scaled)
        
        # 9. Retour à la valeur réelle
        final_predictions = np.expm1(log_pred[0])

        # 10. On retourne la valeur finale à l'utilisateur : C'est un dictionnaire que l'on retourne
        return {"predicted_consumption_kBtu": float(final_predictions)}