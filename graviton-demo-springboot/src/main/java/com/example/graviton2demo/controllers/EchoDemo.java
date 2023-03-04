package com.example.graviton2demo.controllers;

import com.example.graviton2demo.pojo.EchoInoPojo;
import com.example.graviton2demo.services.EchoService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class EchoDemo {
    @Autowired
    private EchoService echoService;
    @GetMapping("/")
    public String echo(){
        EchoInoPojo echoInoPojo = echoService.getEchoInfo();
        String retHtml="<html><body><h1>Graviton University Java Demo</h1>";
        retHtml+="<p>Instance Type : ";
        retHtml+=echoInoPojo.getInstanceType();
        retHtml+="</p><p>Instance ID : ";
        retHtml+=echoInoPojo.getInstanceId();
        retHtml+="</p><p>Runtime is : ";
        retHtml+=echoInoPojo.getRuntime();
        retHtml+="</p><p>OS Version is : ";
        retHtml+=echoInoPojo.getOSVersion();
        retHtml+="</p><p>Instance AZ is : ";
        retHtml+=echoInoPojo.getInstanceAZ();
        retHtml+="</p><p>TimeStamp is : ";
        retHtml+=echoInoPojo.getTimestamp();
        retHtml+="</body></html>";

        return retHtml;
    }
}
