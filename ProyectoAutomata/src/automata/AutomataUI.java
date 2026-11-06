package automata;

import javax.swing.*;
import java.awt.*;
import java.awt.event.*;
import java.util.*;

public class AutomataUI extends JFrame {
    private final DefaultListModel<String> estadosModel;
    private final DefaultListModel<String> alfabetoModel;
    private final JTextField campoEstado;
    private final JTextField campoSimbolo;
    private final JTextField campoOrigen;
    private final JTextField campoDestino;
    private final JTextField campoCadena;
    private final JComboBox<String> comboEstadosIniciales;
    private final DefaultListModel<String> estadosAceptacionModel;
    private final Map<String, Map<String, String>> transiciones;

    public AutomataUI() {
        setTitle("Simulador de Autómata");
        setDefaultCloseOperation(EXIT_ON_CLOSE);
        setLayout(new BorderLayout());

        estadosModel = new DefaultListModel<>();
        alfabetoModel = new DefaultListModel<>();
        estadosAceptacionModel = new DefaultListModel<>();
        transiciones = new HashMap<>();

        JPanel panelPrincipal = new JPanel(new GridLayout(1, 2));

        JPanel panelIzquierdo = new JPanel(new GridLayout(8, 1));
        campoEstado = new JTextField();
        JButton botonAgregarEstado = new JButton("Agregar Estado");
        panelIzquierdo.add(new JLabel("Estado:"));
        panelIzquierdo.add(campoEstado);
        panelIzquierdo.add(botonAgregarEstado);
        JList<String> listaEstados = new JList<>(estadosModel);
        panelIzquierdo.add(new JScrollPane(listaEstados));

        campoSimbolo = new JTextField();
        JButton botonAgregarSimbolo = new JButton("Agregar Símbolo");
        panelIzquierdo.add(new JLabel("Símbolo del alfabeto:"));
        panelIzquierdo.add(campoSimbolo);
        panelIzquierdo.add(botonAgregarSimbolo);
        JList<String> listaAlfabeto = new JList<>(alfabetoModel);
        panelIzquierdo.add(new JScrollPane(listaAlfabeto));

        panelPrincipal.add(panelIzquierdo);

        JPanel panelDerecho = new JPanel(new GridLayout(10, 1));
        campoOrigen = new JTextField();
        campoDestino = new JTextField();
        JTextField campoTransicionSimbolo = new JTextField();
        JButton botonAgregarTransicion = new JButton("Agregar Transición");

        panelDerecho.add(new JLabel("Origen:"));
        panelDerecho.add(campoOrigen);
        panelDerecho.add(new JLabel("Destino:"));
        panelDerecho.add(campoDestino);
        panelDerecho.add(new JLabel("Símbolo de transición:"));
        panelDerecho.add(campoTransicionSimbolo);
        panelDerecho.add(botonAgregarTransicion);

        comboEstadosIniciales = new JComboBox<>();
        panelDerecho.add(new JLabel("Estado Inicial:"));
        panelDerecho.add(comboEstadosIniciales);

        JButton botonEstadoAceptacion = new JButton("Agregar Estado de Aceptación");
        panelDerecho.add(botonEstadoAceptacion);

        JList<String> listaAceptacion = new JList<>(estadosAceptacionModel);
        panelDerecho.add(new JScrollPane(listaAceptacion));

        panelPrincipal.add(panelDerecho);
        add(panelPrincipal, BorderLayout.CENTER);

        JPanel panelInferior = new JPanel();
        campoCadena = new JTextField(10);
        JButton botonSimular = new JButton("Simular");
        JButton botonMostrar = new JButton("Mostrar Configuración del Autómata");
        JButton botonVerDiagrama = new JButton("Ver Diagrama");
        panelInferior.add(new JLabel("Cadena:"));
        panelInferior.add(campoCadena);
        panelInferior.add(botonSimular);
        panelInferior.add(botonMostrar);
        panelInferior.add(botonVerDiagrama);
        add(panelInferior, BorderLayout.SOUTH);

        botonAgregarEstado.addActionListener(e -> {
            String estado = campoEstado.getText().trim();
            if (!estado.isEmpty() && !estadosModel.contains(estado)) {
                estadosModel.addElement(estado);
                comboEstadosIniciales.addItem(estado);
                campoEstado.setText("");
            }
        });

        botonAgregarSimbolo.addActionListener(e -> {
            String simbolo = campoSimbolo.getText().trim();
            if (!simbolo.isEmpty() && !alfabetoModel.contains(simbolo)) {
                alfabetoModel.addElement(simbolo);
                campoSimbolo.setText("");
            }
        });

        botonAgregarTransicion.addActionListener(e -> {
            String origen = campoOrigen.getText().trim();
            String destino = campoDestino.getText().trim();
            String simbolo = campoTransicionSimbolo.getText().trim();
            if (!origen.isEmpty() && !destino.isEmpty() && !simbolo.isEmpty()) {
                transiciones.computeIfAbsent(origen, k -> new HashMap<>()).put(simbolo, destino);
                campoOrigen.setText("");
                campoDestino.setText("");
                campoTransicionSimbolo.setText("");
            }
        });

        botonEstadoAceptacion.addActionListener(e -> {
            String estado = (String) comboEstadosIniciales.getSelectedItem();
            if (estado != null && !estadosAceptacionModel.contains(estado)) {
                estadosAceptacionModel.addElement(estado);
            }
        });

        botonSimular.addActionListener(e -> {
            String cadena = campoCadena.getText().trim();
            String estadoActual = (String) comboEstadosIniciales.getSelectedItem();
            if (estadoActual == null || cadena.isEmpty()) {
                JOptionPane.showMessageDialog(this, "Por favor, seleccione un estado inicial y una cadena.");
                return;
            }

            for (char c : cadena.toCharArray()) {
                if (transiciones.containsKey(estadoActual)) {
                    Map<String, String> transicionesEstadoActual = transiciones.get(estadoActual);
                    String simbolo = String.valueOf(c);
                    if (transicionesEstadoActual.containsKey(simbolo)) {
                        estadoActual = transicionesEstadoActual.get(simbolo);
                    } else {
                        estadoActual = null;
                        break;
                    }
                } else {
                    estadoActual = null;
                    break;
                }
            }

            if (estadoActual != null && estadosAceptacionModel.contains(estadoActual)) {
                JOptionPane.showMessageDialog(this, "Cadena aceptada");
            } else {
                JOptionPane.showMessageDialog(this, "Cadena no aceptada");
            }
        });

        botonMostrar.addActionListener(e -> {
            StringBuilder mensaje = new StringBuilder();

            // Convertir los elementos de los DefaultListModel a una lista
            mensaje.append("Estados: ").append(Collections.list(estadosModel.elements())).append("\n");
            mensaje.append("Alfabeto: ").append(Collections.list(alfabetoModel.elements())).append("\n");
            mensaje.append("Estado Inicial: ").append(comboEstadosIniciales.getSelectedItem()).append("\n");
            mensaje.append("Estados de Aceptación: ").append(Collections.list(estadosAceptacionModel.elements()))
                    .append("\n");
            mensaje.append("Transiciones:\n");

            // Mostrar las transiciones
            for (String origen : transiciones.keySet()) {
                for (String simbolo : transiciones.get(origen).keySet()) {
                    String destino = transiciones.get(origen).get(simbolo);
                    mensaje.append(origen).append(" --").append(simbolo).append("--> ").append(destino).append("\n");
                }
            }

            JOptionPane.showMessageDialog(this, mensaje.toString());
        });

        botonVerDiagrama.addActionListener(e -> {
            JFrame frame = new JFrame("Diagrama del Autómata");
            frame.setSize(600, 400);
            frame.add(new JPanel() {
                protected void paintComponent(Graphics g) {
                    super.paintComponent(g);
                    Graphics2D g2 = (Graphics2D) g;
                    g2.setRenderingHint(RenderingHints.KEY_ANTIALIASING, RenderingHints.VALUE_ANTIALIAS_ON);
                    int radius = 40;
                    Map<String, Point> posiciones = new HashMap<>();
                    int i = 0;
                    for (String estado : Collections.list(estadosModel.elements())) {
                        int x = 100 + (i * 150);
                        int y = 150;
                        posiciones.put(estado, new Point(x, y));
                        g2.drawOval(x, y, radius, radius);
                        g2.drawString(estado, x + 15, y + 25);
                        if (estadosAceptacionModel.contains(estado)) {
                            g2.drawOval(x - 5, y - 5, radius + 10, radius + 10);
                        }
                        i++;
                    }

                    String estadoInicial = (String) comboEstadosIniciales.getSelectedItem();
                    if (estadoInicial != null && posiciones.containsKey(estadoInicial)) {
                        Point p = posiciones.get(estadoInicial);
                        g2.drawLine(p.x - 30, p.y + radius / 2, p.x, p.y + radius / 2);
                        g2.drawString("Inicio", p.x - 50, p.y + radius / 2 - 5);
                    }

                    for (String origen : transiciones.keySet()) {
                        Point p1 = posiciones.get(origen);
                        for (String simbolo : transiciones.get(origen).keySet()) {
                            String destino = transiciones.get(origen).get(simbolo);
                            Point p2 = posiciones.get(destino);
                            if (p1 != null && p2 != null) {
                                g2.drawLine(p1.x + radius / 2, p1.y + radius / 2, p2.x + radius / 2, p2.y + radius / 2);
                                g2.drawString(simbolo, (p1.x + p2.x) / 2, (p1.y + p2.y) / 2);
                            }
                        }
                    }
                }
            });
            frame.setVisible(true);
        });

        setSize(800, 600);
        setLocationRelativeTo(null);
        setVisible(true);
    }

    public static void main(String[] args) {
        SwingUtilities.invokeLater(AutomataUI::new);
    }
}
