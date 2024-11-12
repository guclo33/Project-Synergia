const template = async () => {
    if(accessToken)
    try {
        const templateInfos = await fetch("https://api.canva.com/rest/v1/brand-templates/DAGRszAOv3U/PGhW3Du5l8W830xgiii5ag/dataset", {
            method: "GET",
            headers: {"Authorization" : `Bearer ${accessToken}`}
        });
        const info = await templateInfos.json();
        return info
    } catch (error) {
        console.log(error)
    }
}