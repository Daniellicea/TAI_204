"""
Survival Guide - Programación Móvil
Aventura de texto interactiva con Flask
"""

from flask import Flask, render_template, request, session, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'survival_guide_2026'

# ── Datos de secciones ──

SECTIONS = {
    'reglas': {
        'title': 'La Camara de las Reglas',
        'icon': 'I',
        'questions': [
            {
                'id': 'r1',
                'text': '¿Qué porcentaje mínimo de asistencia se requiere?',
                'options': [('a','50%'),('b','70%'),('c','80%'),('d','90%')],
                'answer': 'c'
            },
            {
                'id': 'r2',
                'text': '¿Cuántos minutos de tolerancia hay al inicio?',
                'options': [('a','5 min'),('b','10 min'),('c','15 min'),('d','20 min')],
                'answer': 'b'
            },
            {
                'id': 'r3',
                'text': '¿Qué consecuencia tiene el plagio?',
                'options': [('a','Advertencia'),('b','Baja de puntos'),('c','Reprobación'),('d','Extraordinario')],
                'answer': 'c'
            },
            {
                'id': 'r4',
                'text': '¿En cuántas horas máximo se justifican faltas?',
                'options': [('a','12 hrs'),('b','24 hrs'),('c','48 hrs'),('d','72 hrs')],
                'answer': 'b'
            },
        ]
    },
    'notas': {
        'title': 'El Oraculo de las Notas',
        'icon': 'II',
        'questions': [
            {
                'id': 'n1',
                'text': '¿Cuánto vale Evidencia de Conocimiento en el 1er parcial?',
                'options': [('a','20%'),('b','30%'),('c','40%'),('d','50%')],
                'answer': 'c'
            },
            {
                'id': 'n2',
                'text': '¿Cuánto vale el Proyecto Integrador en el 3er parcial?',
                'options': [('a','10%'),('b','30%'),('c','40%'),('d','50%')],
                'answer': 'd'
            },
            {
                'id': 'n3',
                'text': '¿Cuánto vale Evidencia de Desempeño en el 2do parcial?',
                'options': [('a','10%'),('b','20%'),('c','30%'),('d','40%')],
                'answer': 'b'
            },
        ]
    },
    'skills': {
        'title': 'Skills a Desbloquear',
        'icon': 'III',
        'questions': [
            {
                'id': 's1',
                'text': '¿Cuál es el objetivo principal de la materia?',
                'options': [('a','Diseñar bases de datos'),('b','Desarrollar apps móviles'),('c','Administrar servidores'),('d','Crear videojuegos')],
                'answer': 'b'
            },
            {
                'id': 's2',
                'text': '¿Qué paradigma de programación se usa?',
                'options': [('a','Funcional'),('b','Lógica'),('c','Orientada a objetos'),('d','Estructurada')],
                'answer': 'c'
            },
            {
                'id': 's3',
                'text': '¿Las soluciones son para una sola plataforma?',
                'options': [('a','Sí, solo Android'),('b','Sí, solo iOS'),('c','No, multiplataforma'),('d','Solo web')],
                'answer': 'c'
            },
        ]
    },
    'timeline': {
        'title': 'La Linea del Tiempo',
        'icon': 'IV',
        'questions': [
            {
                'id': 't1',
                'text': '¿Cuándo es el examen del 1er Parcial?',
                'options': [('a','01-06-26'),('b','06-07-26'),('c','10-08-26'),('d','17-08-26')],
                'answer': 'a'
            },
            {
                'id': 't2',
                'text': '¿Cuándo es el Examen Final?',
                'options': [('a','01-06-26'),('b','06-07-26'),('c','10-08-26'),('d','17-08-26')],
                'answer': 'd'
            },
            {
                'id': 't3',
                'text': '¿Cuándo es el examen del 2do Parcial?',
                'options': [('a','01-06-26'),('b','06-07-26'),('c','10-08-26'),('d','17-08-26')],
                'answer': 'b'
            },
        ]
    },
}

ORDER = ['reglas', 'notas', 'skills', 'timeline']


def get_progress():
    """Obtiene el progreso del usuario desde la sesión."""
    if 'progress' not in session:
        session['progress'] = {
            'reglas':   {'unlocked': True,  'completed': False, 'score': 0},
            'notas':    {'unlocked': False, 'completed': False, 'score': 0},
            'skills':   {'unlocked': False, 'completed': False, 'score': 0},
            'timeline': {'unlocked': False, 'completed': False, 'score': 0},
        }
    return session['progress']


def handle_section(section_key):
    """Lógica genérica para cualquier sección: quiz + confirmación."""
    progress = get_progress()

    if not progress[section_key]['unlocked']:
        flash('Completa el nivel anterior primero.', 'warning')
        return redirect(url_for('index'))

    feedback = {}
    show_confirm = False

    if request.method == 'POST':
        action = request.form.get('action')

        if action == 'submit_quiz':
            correct = 0
            for q in SECTIONS[section_key]['questions']:
                user_ans = request.form.get(q['id'])
                is_correct = user_ans == q['answer']
                if is_correct:
                    correct += 1
                feedback[q['id']] = {'selected': user_ans, 'correct': q['answer'], 'is_correct': is_correct}

            progress[section_key]['score'] = correct
            total = len(SECTIONS[section_key]['questions'])

            if correct >= 2:
                show_confirm = True
                flash(f'{correct}/{total} correctas. Confirma para avanzar.', 'success')
            else:
                flash(f'{correct}/{total} correctas. Necesitas minimo 2.', 'danger')
            session['progress'] = progress

        elif action == 'confirm':
            if request.form.get('confirm_check'):
                progress[section_key]['completed'] = True
                idx = ORDER.index(section_key)
                if idx + 1 < len(ORDER):
                    progress[ORDER[idx + 1]]['unlocked'] = True
                session['progress'] = progress
                if section_key == 'timeline':
                    flash('Aventura completada. Estas listo para Programacion Movil.', 'success')
                else:
                    flash('Nivel completado. Siguiente nivel desbloqueado.', 'success')
                return redirect(url_for('index'))
            else:
                show_confirm = True
                flash('Marca la casilla de confirmacion.', 'warning')

    if progress[section_key]['score'] >= 2 and not progress[section_key]['completed']:
        show_confirm = True

    completed_count = sum(1 for s in progress.values() if s['completed'])
    return render_template(f'{section_key}.html',
                           section=SECTIONS[section_key],
                           progress=progress[section_key],
                           feedback=feedback,
                           show_confirm=show_confirm,
                           completed=completed_count)


# ── Rutas ──

@app.route('/')
def index():
    progress = get_progress()
    completed = sum(1 for s in progress.values() if s['completed'])
    return render_template('index.html', progress=progress, sections=SECTIONS,
                           order=ORDER, completed=completed)

@app.route('/reset')
def reset():
    session.clear()
    flash('Aventura reiniciada.', 'info')
    return redirect(url_for('index'))

@app.route('/reglas', methods=['GET', 'POST'])
def reglas():
    return handle_section('reglas')

@app.route('/notas', methods=['GET', 'POST'])
def notas():
    return handle_section('notas')

@app.route('/skills', methods=['GET', 'POST'])
def skills():
    return handle_section('skills')

@app.route('/timeline', methods=['GET', 'POST'])
def timeline():
    return handle_section('timeline')


if __name__ == '__main__':
    app.run(debug=True, port=5000)
