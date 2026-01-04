package com.quantitative.domain;

/**
 * Configuración inmutable para la simulación de Montecarlo.
 * Define los parámetros financieros y técnicos de la ejecución.
 */
public record SimulationConfig(
        double initialPrice,       // Precio inicial del activo (S0)
        double volatility,         // Volatilidad anualizada (sigma)
        double expectedReturn,     // Retorno esperado anualizado (mu)
        double timeHorizon,        // Horizonte de tiempo en años (T)
        int numSimulations,        // Número de trayectorias a simular (N)
        int numSteps               // Pasos de tiempo dentro del horizonte (dt)
) {
    // Constructor compacto para validaciones de "Fail Fast"
    public SimulationConfig {
        if (initialPrice <= 0) throw new IllegalArgumentException("El precio inicial debe ser positivo.");
        if (volatility < 0) throw new IllegalArgumentException("La volatilidad no puede ser negativa.");
        if (timeHorizon <= 0) throw new IllegalArgumentException("El horizonte de tiempo debe ser positivo.");
        if (numSimulations <= 0) throw new IllegalArgumentException("El número de simulaciones debe ser positivo.");
        if (numSteps <= 0) throw new IllegalArgumentException("El número de pasos debe ser positivo.");
    }
}