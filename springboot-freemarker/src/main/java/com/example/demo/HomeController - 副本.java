package com.example.demo;

import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;

@Controller
public class HomeController {

    @GetMapping("/")
    public String home(@RequestParam(value = "value", defaultValue = "hello") String value, Model model) {
        model.addAttribute("msg", value);
        return "home";  // this refers to home.ftl
    }
}