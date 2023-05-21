package com.example.demo;

import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;

@Controller
public class HomeController {

    @GetMapping("/")
    public String home(Model model) {
        model.addAttribute("msg", "Enter your message");
        return "home";
    }

    @PostMapping("/process")
    @ResponseBody
    public String process(@RequestParam String userInput) {
        // Sanitize and process the user input here
        return userInput;  // Return the processed input
    }
}