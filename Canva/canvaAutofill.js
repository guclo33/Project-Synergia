const fetch = (...args) => import('node-fetch').then(({default: fetch}) => fetch(...args));
const {Client} = require("pg");
require("dotenv").config()

const client = new Client ({
    host : process.env.DB_HOST,
    port : process.env.DB_PORT,
    user : process.env.DB_USER,
    password : process.env.DB_PASSWORD,
    database : process.env.DB_DATABASE
})



const autofillJob = async (accessToken, templateId) => {
    try {
    const autofillPost = await fetch('https://api.canva.com/rest/v1/autofills', {
        method : "POST",
        headers : {
            "Autorization" : `Bearer ${accessToken}`,
            "Content-Type" : "application/json"
        },
        data : {
            "brand_template_id": `${templateId}`,
            "title": "",
            "data": {
                "motivationsNaturelles": {
                    "type": "text",
                    "text": ""
                },
                "nomClient": {
                    "type": "text",
                    "text": ""
                },
                "nomPersonalite": {
                    "type": "text",
                    "text": ""
                },
                "enBref": {
                    "type": "text",
                    "text": ""
                },
                "valeurCouleur": {
                    "type": "chart",
                    "chart_data": {
                        "rows": [
                          {
                            "cells": [
                              {
                                "type": "number",
                                "value": 
                              },
                              {
                                "type": "number",
                                "value": 
                              },
                              {
                                "type": "number",
                                "value": 
                              },
                              {
                                "type": "number",
                                "value": 
                              }
                            ]}
                        ]}}
                ,
                "forcesEnLumieres": {
                    "type": "text",
                    "text": ""
                },
                "defisPotentiels": {
                    "type": "text",
                    "text": ""
                },
                "perceptionChangement": {
                    "type": "text",
                    "text": ""
                },
                "relationsInterpersonnelles": {
                    "type": "text",
                    "text": ""
                },
                "perceptionStructure": {
                    "type": "text",
                    "text": ""
                },
                "perceptionProblemes": {
                    "type": "text",
                    "text": ""
                },
                "resume": {
                    "type": "text",
                    "text": ""
                },
                "archNum1": {
                    "type": "text",
                    "text": ""
                },
                "archNum2": {
                    "type": "text",
                    "text": ""
                },
                "textArch1": {
                    "type": "text",
                    "text": ""
                },
                "textArch2": {
                    "type": "text",
                    "text": ""
                },
                "toiTravail": {
                    "type": "text",
                    "text": ""
                },
                "adapte1": {
                    "type": "text",
                    "text": ""
                },
                "adapte2": {
                    "type": "text",
                    "text": ""
                },
                "adapte3": {
                    "type": "text",
                    "text": ""
                },
                "adapte1Titre": {
                    "type": "text",
                    "text": ""
                }
            }
        }
    });

    } catch (err) {
        console.error("Could not start autofill job", err)
    }
}