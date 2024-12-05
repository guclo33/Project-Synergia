import React, {useState} from "react";


export function Profile({detailsData}) {
    const [view, setView] = useState(false)
    const {info} = detailsData
    
    const handleClick = () => {
        setView(!view)
    }

    return(
        <div className="profile">
            <button onClick={handleClick}>Voir profile</button>
            {view ? (
            <>
            <h2>Profile Synergia :</h2>
            <div className="couleur">
                <h4>Couleur:</h4>
                <p>bleu : {info.bleu}</p><p>vert : {info.vert}</p><p>jaune : {info.jaune}</p><p>rouge : {info.rouge}</p>
            </div>
            <div className="archétype">
                <h4>Vos deux pricipaux archétypes:</h4>
                <p>{info.archnum1}</p><p>{info.archnum2}</p>
            </div>
            <div className="texteProfile">
                <h5>En bref :</h5>
                <p>{info.enbref}</p>
                <h5>Tes forces mis en lumière:</h5>
                <p>{info.forcesenlumieres}</p>
                <h5>Tes défis portentiels:</h5>
                <p>{info.defispotentiels}</p>
                <h5>Perception du changement:</h5>
                <p>{info.perceptionchangement}</p>
                <h5>Perception des relations interpersonnelles :</h5>
                <p>{info.relationsinterpersonnelles}</p>
                <h5>Perception de la structure et de la prévisibilité :</h5>
                <p>{info.perceptionstructure}</p>
                <h5>Perceptions des défis, problèmes et difficultés :</h5>
                <p>{info.perceptionproblemes}</p>
                <h4>Tes archétype</h4>
                <h5>Tes motivations naturelle :</h5>
                <p>{info.motivationsnaturelles}</p>
                <h5>{info.archnum1}</h5>
                <p>{info.textarch1}</p>
                <h5>{info.archnum2}</h5>
                <p>{info.textarch2}</p>
                <h5>Toi et le marché du travail</h5>
                <p>{info.toitravail}</p>
                <h5>S'adapter au rouge</h5>
                <p>{info.adapterouge}</p>
                <h5>S'adapter au bleu</h5>
                <p>{info.adaptebleu}</p>
                <h5>S'adapter au vert</h5>
                <p>{info.adaptevert}</p>
                <h5>S'adapter au jaune</h5>
                <p>{info.adaptejaune}</p>
                <p></p>
            </div>
            </>
            ) : null}

        </div>
    )
}