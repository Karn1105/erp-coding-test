package com.erp.controller;

import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;
import java.util.List;
import java.util.Map;

@RestController
public class InventoryController {

    private final JdbcTemplate jdbcTemplate;

    // Injecting JdbcTemplate via constructor
    public InventoryController(JdbcTemplate jdbcTemplate) {
        this.jdbcTemplate = jdbcTemplate;
    }

    /**
     * Implemented method:
     * 1. Query 'inventory' table where quantity <= reorder_level.
     * 2. Return List of Maps representing JSON objects.
     */
    @GetMapping("/api/inventory/alerts")
    public List<Map<String, Object>> getAlerts() {
        String sql = "SELECT * FROM inventory WHERE quantity <= reorder_level";
        return jdbcTemplate.queryForList(sql);
    }
}
