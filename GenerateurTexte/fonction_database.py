import psycopg2

conn = psycopg2.connect(
    dbname="Synergie_MLM",
    user="postgres",
    password="breekel123",
    host="localhost"
)
cursor = conn.cursor()

def update_database (nom_profile, motivation_text, bref_text, forces_text, defis_text, changements_text, interpersonnelles_text, structure_text, problemes_text, arch1_nom, arch2_nom, desc_arch1_text, desc_arch2_text, travail_text, adapte_rouge_text, adapte_bleu_text, adapte_vert_text, adapte_jaune_text, bleu, rouge, jaune, vert, explorateur, protecteur, bouffon, souverain, magicien, createur, hero, citoyen, sage, amoureuse, rebelle, optimiste , email, nom_leader) :
    
    cursor.execute(
        """WITH ins AS (
            INSERT INTO client (nom_client, email)
            VALUES (%s, %s) 
            ON CONFLICT (nom_client, email) DO NOTHING 
            RETURNING id
        ) 
        SELECT id FROM ins 
        UNION ALL 
        SELECT id FROM client WHERE nom_client = %s AND email = %s;""", (nom_profile, email, nom_profile, email)
    )
    client_id = cursor.fetchone()[0]
    
    
    cursor.execute("INSERT INTO leader (nom_leader) VALUES (%s) ON CONFLICT (nom_leader) DO NOTHING", (nom_leader,))
        


    # Insérer les données dans la table
    cursor.execute(
        "INSERT INTO profile (nomclient, motivationsnaturelles, enbref,  forcesenlumieres, defispotentiels, perceptionchangement, relationsinterpersonnelles, perceptionstructure, perceptionproblemes, archnum1, archnum2, textarch1, textarch2, toitravail, adapterouge, adaptebleu, adaptevert, adaptejaune, bleu, rouge, jaune, vert, explorateur, protecteur, bouffon, souverain, magicien, createur, hero, citoyen, sage, amoureuse, rebelle, optimiste ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id",
        (nom_profile, motivation_text, bref_text, forces_text, defis_text, changements_text, interpersonnelles_text, structure_text, problemes_text, arch1_nom, arch2_nom, desc_arch1_text, desc_arch2_text, travail_text, adapte_rouge_text, adapte_bleu_text, adapte_vert_text, adapte_jaune_text, bleu, rouge, jaune, vert, explorateur, protecteur, bouffon, souverain, magicien, createur, hero, citoyen, sage, amoureuse, rebelle, optimiste )
    )
    profile_id = cursor.fetchone()[0]
    
    cursor.execute("INSERT INTO client_profile (client_id, profile_id) VALUES (%s, %s)", (client_id, profile_id))
    

    # Valider les changements et fermer la connexion
    conn.commit()
    cursor.close()
    conn.close()

