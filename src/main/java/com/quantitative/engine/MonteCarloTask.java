package com.quantitative.engine;

import com.quantitative.domain.SimulationConfig;
import java.util.Random;
import java.util.concurrent.Callable;

/**
 * Tarea computacional que ejecuta una única simulación de trayectoria de precio.
 * Utiliza el modelo de Movimiento Browniano Geométrico (GBM).
 * Implementa Callable para poder ser ejecutada en paralelo.
 */
public class MonteCarloTask implements Callable<Double> {

    private final SimulationConfig config;
    private final Random random;

    public MonteCarloTask(SimulationConfig config, Random random) {
        this.config = config;
        this.random = random;
    }

    @Override
    public Double call() {
        double currentPrice = config.initialPrice();
        double dt = config.timeHorizon() / config.numSteps();

        // Pre-cálculo de términos constantes para optimizar rendimiento dentro del bucle
        // Drift: (mu - sigma^2 / 2) * dt
        double drift = (config.expectedReturn() - 0.5 * Math.pow(config.volatility(), 2)) * dt;
        // Volatility: sigma * sqrt(dt)
        double vol = config.volatility() * Math.sqrt(dt);

        // Bucle principal de simulación (trayectoria paso a paso)
        for (int i = 0; i < config.numSteps(); i++) {
            double standardNormal = random.nextGaussian(); // Z ~ N(0,1)
            // Fórmula GBM: S_t = S_{t-1} * exp(drift + vol * Z)
            currentPrice = currentPrice * Math.exp(drift + vol * standardNormal);
        }

        return currentPrice;
    }
}