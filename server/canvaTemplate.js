const fs = require('fs');
const fetch = (...args) => import('node-fetch').then(({ default: fetch }) => fetch(...args));



const templateDataset = async (templateId, accessToken, refreshToken) => {
    const templateInfos = await fetch(`https://api.canva.com/rest/v1/brand-templates/${templateId}/dataset`,   {
    method: "GET",
    headers: {"Authorization" : `Bearer ${accessToken}`}
    });
        if (!templateInfos.ok) {
            console.error("Error fetching template information:", templateInfos.status, templateInfos.statusText);
            return;
        }


        const info = await templateInfos.json();
        console.log (info)
        fs.writeFileSync('accessToken.json', JSON.stringify({ accessToken: accessToken, refreshToken: refreshToken, templateId : templateId }));
        return info
    }; 


const template = async (accessToken, refreshToken) => {
    let templateId = ""
    if (!accessToken) {
        console.error("Access token is undefined or missing.");
        return;
    }
    try {
        
        const getTemplateId = await fetch("https://api.canva.com/rest/v1/brand-templates",
            {
                method: "GET",
                headers : {
                    "Authorization" : `Bearer ${accessToken}`
                }
            }
        );
        const templateIdInfos = await getTemplateId.json()
        templateId = await templateIdInfos.items[0].id;
        console.log(templateIdInfos);
        try {
            templateDataset(templateId, accessToken, refreshToken);
        } catch (err) {
            console.log("Could not get template dataset", err)
        }
        

    } catch(err) {
        console.log("Could not get template id", err)
    }
     
}





module.exports = {
    template
}