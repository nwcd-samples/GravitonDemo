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
    public EchoInoPojo echo(){
        EchoInoPojo echoInoPojo = echoService.getEchoInfo();

        return echoInoPojo;
    }
}
