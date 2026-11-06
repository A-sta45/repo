package automata;
import javax.swing.*;
import java.awt.*;
import java.awt.event.*;
import java.util.ArrayList;
import java.util.List;

public class AutomataPanel extends JPanel {

    private List<EstadoVisual> estados = new ArrayList<>();
    private List<Transicion> transiciones = new ArrayList<>();
    private int contadorEstados = 0;
    private final int RADIO = 40;

    public AutomataPanel() {
        setBackground(new Color(220, 220, 220));
        setLayout(null);

        addMouseListener(new MouseAdapter() {
            @Override
            public void mouseClicked(MouseEvent e) {
                // Crear un nuevo estado al hacer clic
                String nombreEstado = "q" + contadorEstados++;
                EstadoVisual nuevo = new EstadoVisual(nombreEstado, e.getX(), e.getY());
                estados.add(nuevo);
                repaint();
            }
        });

        // Ejemplo de transición manual (agregar en tu lógica de transición)
        // En este caso, se agrega una transición entre q0 y q1 con el símbolo 'a'
        // Esto es solo para prueba.
        // En la lógica real, debes agregar transiciones según la entrada del usuario.
        if (estados.size() > 1) {
            transiciones.add(new Transicion(estados.get(0), estados.get(1), "a"));
        }
    }

    @Override
    protected void paintComponent(Graphics g) {
        super.paintComponent(g);

        Graphics2D g2 = (Graphics2D) g;
        g2.setFont(new Font("Arial", Font.BOLD, 14));

        // Dibujar los estados
        for (EstadoVisual estado : estados) {
            int x = estado.x - RADIO / 2;
            int y = estado.y - RADIO / 2;

            g2.setColor(Color.WHITE);
            g2.fillOval(x, y, RADIO, RADIO);

            g2.setColor(Color.BLACK);
            g2.drawOval(x, y, RADIO, RADIO);

            FontMetrics fm = g2.getFontMetrics();
            int textoAncho = fm.stringWidth(estado.nombre);
            int textoAlto = fm.getAscent();
            g2.drawString(estado.nombre, estado.x - textoAncho / 2, estado.y + textoAlto / 4);
        }

        // Dibujar las transiciones
        for (Transicion trans : transiciones) {
            EstadoVisual origen = trans.origen;
            EstadoVisual destino = trans.destino;

            // Dibujar la línea de la transición
            g2.setColor(Color.BLACK);
            g2.drawLine(origen.x, origen.y, destino.x, destino.y);

            // Dibujar la flecha
            drawArrow(g2, origen.x, origen.y, destino.x, destino.y);

            // Dibujar el símbolo de la transición en el medio de la línea
            String simbolo = trans.simbolo;
            int middleX = (origen.x + destino.x) / 2;
            int middleY = (origen.y + destino.y) / 2;
            FontMetrics fm = g2.getFontMetrics();
            int textoAncho = fm.stringWidth(simbolo);
            int textoAlto = fm.getAscent();
            g2.drawString(simbolo, middleX - textoAncho / 2, middleY + textoAlto / 4);
        }
    }

    // Método para dibujar una flecha entre dos puntos (x1, y1) y (x2, y2)
    private void drawArrow(Graphics2D g2, int x1, int y1, int x2, int y2) {
        // Dibujar la línea principal
        g2.drawLine(x1, y1, x2, y2);

        // Dibujar las flechas en el extremo de la línea
        int arrowSize = 10;
        double angle = Math.atan2(y2 - y1, x2 - x1);
        int x1Arrow = (int) (x2 - arrowSize * Math.cos(angle - Math.PI / 6));
        int y1Arrow = (int) (y2 - arrowSize * Math.sin(angle - Math.PI / 6));
        int x2Arrow = (int) (x2 - arrowSize * Math.cos(angle + Math.PI / 6));
        int y2Arrow = (int) (y2 - arrowSize * Math.sin(angle + Math.PI / 6));

        g2.drawLine(x2, y2, x1Arrow, y1Arrow);
        g2.drawLine(x2, y2, x2Arrow, y2Arrow);
    }

    // Clase para representar un estado visual
    private static class EstadoVisual {
        String nombre;
        int x, y;

        EstadoVisual(String nombre, int x, int y) {
            this.nombre = nombre;
            this.x = x;
            this.y = y;
        }
    }

    // Clase para representar una transición entre dos estados
    private static class Transicion {
        EstadoVisual origen;
        EstadoVisual destino;
        String simbolo;

        Transicion(EstadoVisual origen, EstadoVisual destino, String simbolo) {
            this.origen = origen;
            this.destino = destino;
            this.simbolo = simbolo;
        }
    }
}
