import React, { useEffect, useRef, useState } from 'react';
import { Heart, Calendar, Gift, Trash2, Edit3, Plus, Bell, X, Check } from 'lucide-react';
import axios from 'axios';
import '@/App.css';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

function App() {
  const name = 'Yennifer';
  const birthDateStr = '2008-10-12';
  const startDateStr = '2025-10-12';
  const showPhoto = true;
  const photoUrl = 'https://customer-assets.emergentagent.com/job_rose-animation-1/artifacts/g6dosa45_image.png';
  const notificationEmail = 'Yuenortiz252@gmail.com';

  // Crear fechas usando año, mes-1, día para evitar problemas de zona horaria
  const startDate = useRef(new Date(2025, 9, 12)); // Octubre es mes 9 (0-indexed)
  const birthDate = useRef(new Date(2008, 9, 12)); // Octubre es mes 9

  // Estados
  const [comments, setComments] = useState({});
  const [canEdit, setCanEdit] = useState(false);
  const [dateCheckMessage, setDateCheckMessage] = useState('');
  const [editingYear, setEditingYear] = useState(null);
  const [commentText, setCommentText] = useState('');
  const [showNotification, setShowNotification] = useState(false);
  const [notificationMessage, setNotificationMessage] = useState('');
  const [notificationsEnabled, setNotificationsEnabled] = useState(false);

  // Calculate age at startDate
  const calculateAge = (bd, refDate) => {
    let age = refDate.getFullYear() - bd.getFullYear();
    const m = refDate.getMonth() - bd.getMonth();
    if (m < 0 || (m === 0 && refDate.getDate() < bd.getDate())) age--;
    return age;
  };

  const currentAge = calculateAge(birthDate.current, startDate.current);

  // Generate birthdays between currentAge and 100
  const generateFutureBirthdays = () => {
    const arr = [];
    for (let age = currentAge; age <= 100; age++) {
      const year = birthDate.current.getFullYear() + age;
      const date = new Date(year, birthDate.current.getMonth(), birthDate.current.getDate());
      arr.push({
        age,
        year,
        date,
        formatted: date.toLocaleDateString('es-ES', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' })
      });
    }
    return arr;
  };

  const futureBirthdays = useRef(generateFutureBirthdays());

  // animation state
  const [typedText, setTypedText] = useState('');
  const [showRose, setShowRose] = useState(false);
  const [showBirthdays, setShowBirthdays] = useState(false);
  const [isPlaying, setIsPlaying] = useState(false);

  const message = `¡Feliz cumpleaños ${name}, mi hermana querida por siempre!`;

  const timeouts = useRef([]);
  const listRef = useRef(null);

  // Initialize person and load comments
  useEffect(() => {
    initializePerson();
    checkBirthdayDate();
    loadComments();
    startSequence();
    requestNotificationPermission();
    return cleanup;
  }, []);

  // Request notification permission
  function requestNotificationPermission() {
    if ('Notification' in window) {
      if (Notification.permission === 'granted') {
        setNotificationsEnabled(true);
      } else if (Notification.permission === 'default') {
        Notification.requestPermission().then(permission => {
          if (permission === 'granted') {
            setNotificationsEnabled(true);
            showNotificationAlert('✅ Notificaciones habilitadas');
            console.log('Notificaciones habilitadas');
          }
        });
      }
    }
  }

  function enableNotifications() {
    if ('Notification' in window) {
      Notification.requestPermission().then(permission => {
        if (permission === 'granted') {
          setNotificationsEnabled(true);
          showNotificationAlert('✅ Notificaciones habilitadas exitosamente');
          showBrowserNotification(
            '🔔 Notificaciones Activadas',
            `Recibirás recordatorios del cumpleaños de ${name}.`
          );
        } else {
          alert('Por favor permite las notificaciones en la configuración de tu navegador');
        }
      });
    } else {
      alert('Tu navegador no soporta notificaciones');
    }
  }

  // Show browser notification
  function showBrowserNotification(title, body) {
    if ('Notification' in window && Notification.permission === 'granted') {
      new Notification(title, {
        body: body,
        icon: 'https://em-content.zobj.net/source/apple/391/rose_1f339.png',
        badge: 'https://em-content.zobj.net/source/apple/391/birthday-cake_1f382.png',
      });
    }
  }

  async function initializePerson() {
    try {
      await axios.post(`${API}/birthday/person`, {
        name,
        birth_date: birthDateStr,
        start_date: startDateStr,
        photo_url: photoUrl,
        show_photo: showPhoto
      });
    } catch (error) {
      console.error('Error initializing person:', error);
    }
  }

  async function checkBirthdayDate() {
    try {
      const response = await axios.get(`${API}/birthday/check-date/${name}`);
      setCanEdit(response.data.can_edit);
      setDateCheckMessage(response.data.message);
      
      if (response.data.is_birthday) {
        showNotificationAlert('🎉 ¡HOY ES EL CUMPLEAÑOS DE ' + name.toUpperCase() + '! 🎂');
        showBrowserNotification(
          `🎉 ¡Cumpleaños de ${name}!`,
          `¡Hoy ${name} cumple años! No olvides agregar un comentario sobre cómo estuvo la celebración.`
        );
        // Enviar notificación por email
        sendEmailNotification();
      }
    } catch (error) {
      console.error('Error checking date:', error);
    }
  }

  async function sendEmailNotification() {
    try {
      await axios.post(`${API}/birthday/send-notification`, {
        email: notificationEmail,
        person_name: name
      });
    } catch (error) {
      console.error('Error sending email notification:', error);
    }
  }

  async function loadComments() {
    try {
      const response = await axios.get(`${API}/birthday/comments/${name}`);
      const commentsMap = {};
      response.data.forEach(comment => {
        commentsMap[comment.year] = comment;
      });
      setComments(commentsMap);
    } catch (error) {
      console.error('Error loading comments:', error);
    }
  }

  async function saveComment(year, age) {
    if (!commentText.trim()) {
      alert('Por favor escribe un comentario');
      return;
    }

    try {
      await axios.post(`${API}/birthday/comment`, {
        person_name: name,
        year,
        age,
        comment: commentText.trim()
      });
      
      // Reload comments
      await loadComments();
      setCommentText('');
      setEditingYear(null);
      showNotificationAlert('✅ Comentario guardado exitosamente');
      showBrowserNotification(
        '✅ Comentario Guardado',
        `Tu comentario del cumpleaños ${age} ha sido guardado permanentemente.`
      );
    } catch (error) {
      if (error.response?.status === 403) {
        alert(error.response.data.detail);
      } else {
        alert('Error al guardar el comentario');
      }
      console.error('Error saving comment:', error);
    }
  }

  function startEdit(year, age, existingComment = '') {
    // EXCEPCIÓN: El año de 17 siempre se puede editar
    if (age === 17) {
      setEditingYear(year);
      setCommentText(existingComment);
      return;
    }
    
    // Para otros años, verificar si es 12 de octubre
    if (!canEdit) {
      alert('Solo puedes editar comentarios el 12 de octubre (excepto el de 17 años que siempre puedes editar)');
      return;
    }
    setEditingYear(year);
    setCommentText(existingComment);
  }

  function cancelEdit() {
    setEditingYear(null);
    setCommentText('');
  }

  function showNotificationAlert(msg) {
    setNotificationMessage(msg);
    setShowNotification(true);
    setTimeout(() => setShowNotification(false), 5000);
  }

  function cleanup() {
    timeouts.current.forEach((t) => clearTimeout(t));
    timeouts.current = [];
  }

  function typeByWords(text, onComplete) {
    cleanup();
    setTypedText('');
    setShowRose(false);
    setShowBirthdays(false);
    setIsPlaying(true);

    const words = text.split(' ');
    let totalDelay = 0;

    words.forEach((word, wi) => {
      for (let i = 0; i < word.length; i++) {
        const delay = totalDelay + i * 40;
        timeouts.current.push(
          setTimeout(() => setTypedText((prev) => prev + word[i]), delay)
        );
      }
      totalDelay += word.length * 40 + 120;
      timeouts.current.push(
        setTimeout(() => setTypedText((prev) => prev + (wi === words.length - 1 ? '' : ' ')), totalDelay - 60)
      );
    });

    timeouts.current.push(
      setTimeout(() => {
        setIsPlaying(false);
        if (onComplete) onComplete();
      }, totalDelay + 200)
    );
  }

  function startSequence() {
    typeByWords(message, () => {
      timeouts.current.push(setTimeout(() => setShowRose(true), 450));
      timeouts.current.push(setTimeout(() => setShowRose(false), 3650));
      timeouts.current.push(setTimeout(() => {
        setShowBirthdays(true);
        requestAnimationFrame(() => {
          if (listRef.current) listRef.current.scrollTop = 0;
          const items = listRef.current?.querySelectorAll('.birthday-item');
          items?.forEach((el, idx) => setTimeout(() => el.classList.add('appear'), idx * 30));
        });
      }, 3850));
    });
  }

  function handleReplay() {
    cleanup();
    const items = listRef.current?.querySelectorAll('.birthday-item');
    items?.forEach((el) => el.classList.remove('appear'));
    setTypedText('');
    setShowRose(false);
    setShowBirthdays(false);
    setTimeout(startSequence, 160);
  }

  function scrollList(amount = 200) {
    if (!listRef.current) return;
    listRef.current.scrollBy({ top: amount, behavior: 'smooth' });
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-black via-purple-900 to-black p-6 flex items-start justify-center">
      {/* Notification */}
      {showNotification && (
        <div className="fixed top-6 right-6 z-50 bg-gradient-to-r from-purple-700 to-blue-900 text-white px-6 py-4 rounded-lg shadow-2xl flex items-center gap-3 animate-slide-in">
          <Bell className="w-6 h-6" />
          <span className="font-semibold">{notificationMessage}</span>
          <button onClick={() => setShowNotification(false)} className="ml-2">
            <X className="w-5 h-5" />
          </button>
        </div>
      )}

      <div className="w-full max-w-6xl bg-[rgba(0,0,0,0.45)] rounded-2xl p-6 shadow-2xl border border-[rgba(147,51,234,0.2)]">
        <div className="flex items-center gap-4 mb-4">
          <div className="w-14 h-14 rounded-lg bg-gradient-to-br from-purple-600 to-blue-800 flex items-center justify-center font-bold text-white text-2xl">Y</div>
          <div>
            <h1 className="text-2xl font-extrabold text-white">Tarjeta de cumpleaños — {name}</h1>
          </div>
          <div className="ml-auto flex items-center gap-3">
            {!notificationsEnabled && (
              <button
                onClick={enableNotifications}
                className="flex items-center gap-2 px-2 py-2 rounded-md bg-gradient-to-r from-purple-600 to-blue-700 text-white font-semibold shadow-lg hover:shadow-xl transition-all"
                title="Habilitar notificaciones"
              >
                <Bell className="w-5 h-5" />
                <span className="hidden md:inline">Habilitar Notificaciones</span>
              </button>
            )}
            {notificationsEnabled && (
              <div className="flex items-center gap-2 px-2 py-2 rounded-md bg-green-600/30 text-green-300 border border-green-500/50">
                <Bell className="w-5 h-5" />
                <span className="hidden md:inline text-sm">Notificaciones ON</span>
              </div>
            )}
            <div className="text-sm text-slate-400 text-right">
              <div>Generado: {startDate.current.toLocaleDateString('es-ES')}</div>
              {canEdit && <div className="text-green-400 font-semibold mt-1">✓ Hoy puedes editar</div>}
            </div>
          </div>
        </div>

        {dateCheckMessage && (
          <div className={`mb-4 p-3 rounded-lg text-sm ${canEdit ? 'bg-green-900/30 text-green-300 border border-green-700/50' : 'bg-purple-900/30 text-purple-300 border border-purple-700/50'}`}>
            {dateCheckMessage}
          </div>
        )}

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {/* LEFT: Visual area */}
          <div className="md:col-span-1 bg-[rgba(147,51,234,0.05)] rounded-xl p-4 relative overflow-hidden flex flex-col items-center border border-purple-800/30">
            <div className="w-full h-auto flex items-center justify-center px-2 mb-4">
              <pre className="text-xs sm:text-sm md:text-lg lg:text-xl font-semibold text-transparent bg-clip-text bg-gradient-to-r from-purple-300 to-blue-300 leading-tight sm:leading-normal text-center whitespace-pre-wrap mb-2">
                {typedText || ' '}
                {isPlaying && <span className="inline-block animate-pulse text-white">|</span>}
              </pre>
            </div>

            {showPhoto && photoUrl ? (
              <img src={photoUrl} alt={name} className="w-64 h-64 rounded-md object-cover shadow-lg overflow-hidden border-2 border-purple-600/50" />
            ) : (
              <div className="w-64 h-64 rounded-md flex items-center justify-center bg-gradient-to-br from-purple-700 to-blue-900 text-white shadow-inner relative overflow-hidden">
                <div className={`realistic-rose-inline transition-all duration-600 ease-in-out transform ${showRose ? 'opacity-100 scale-100 translate-y-0' : 'opacity-0 scale-90 translate-y-6'}`} aria-hidden="true">
                  <div className="rose-wrapper" style={{width: 240, height: 300}}>
                    <div className="light light1" />
                    <div className="light light2" />
                    <div className="light light3" />

                    <div className="particle particle1" />
                    <div className="particle particle2" />
                    <div className="particle particle3" />
                    <div className="particle particle4" />
                    <div className="particle particle5" />

                    <div className="rose-container">
                      <div className="stem">
                        <div className="thorn thorn1" />
                        <div className="thorn thorn2" />
                        <div className="thorn thorn3" />
                      </div>
                      <div className="leaf left" style={{'--tx': '-100%', '--rot': '-30deg'}} />
                      <div className="leaf right" style={{'--tx': '6px', '--rot': '150deg'}} />

                      <div className="rose">
                        <div className="petal-outer petal-outer1" style={{'--rot': '-10deg'}} />
                        <div className="petal-outer petal-outer2" style={{'--rot': '60deg'}} />
                        <div className="petal-outer petal-outer3" style={{'--rot': '120deg'}} />
                        <div className="petal-outer petal-outer4" style={{'--rot': '180deg'}} />
                        <div className="petal-outer petal-outer5" style={{'--rot': '240deg'}} />
                        <div className="petal-outer petal-outer6" style={{'--rot': '300deg'}} />

                        <div className="petal-mid petal-mid1" style={{'--rot': '20deg'}} />
                        <div className="petal-mid petal-mid2" style={{'--rot': '80deg'}} />
                        <div className="petal-mid petal-mid3" style={{'--rot': '140deg'}} />
                        <div className="petal-mid petal-mid4" style={{'--rot': '200deg'}} />
                        <div className="petal-mid petal-mid5" style={{'--rot': '260deg'}} />
                        <div className="petal-mid petal-mid6" style={{'--rot': '320deg'}} />

                        <div className="petal-inner petal-inner1" style={{'--rot': '30deg'}} />
                        <div className="petal-inner petal-inner2" style={{'--rot': '90deg'}} />
                        <div className="petal-inner petal-inner3" style={{'--rot': '150deg'}} />
                        <div className="petal-inner petal-inner4" style={{'--rot': '210deg'}} />
                        <div className="petal-inner petal-inner5" style={{'--rot': '270deg'}} />
                        <div className="petal-inner petal-inner6" style={{'--rot': '330deg'}} />

                        <div className="center" />
                      </div>
                    </div>
                  </div>
                </div>

                {!showRose && <div className="text-2xl font-bold">🌹</div>}
              </div>
            )}

            <div className="mt-3 text-sm text-slate-300">Pulsa <button className="underline hover:text-purple-400" onClick={handleReplay}>Reproducir</button> para repetir</div>
          </div>

          {/* RIGHT: list + controls */}
          <div className="md:col-span-2 flex flex-col gap-4">
            <div className="flex items-center justify-between gap-4">
              <div>
                <h2 className="text-lg font-bold text-white">Próximos cumpleaños ({currentAge} → 100)</h2>
                <div className="text-sm text-slate-400">Comenzando: <strong>{startDate.current.toLocaleDateString('es-ES')}</strong> — Hoy cumple <strong>{currentAge}</strong></div>
              </div>

              <div className="flex items-center gap-2">
                <button onClick={handleReplay} className="px-3 py-2 rounded-md bg-gradient-to-r from-purple-600 to-blue-700 text-white font-semibold shadow hover:shadow-lg transition-all">Reproducir</button>
                <button onClick={() => window.print()} className="px-3 py-2 rounded-md border border-purple-700/50 text-slate-200 hover:bg-purple-800/20 transition-all">Imprimir</button>
              </div>
            </div>

            <div className="bg-[rgba(147,51,234,0.05)] rounded-lg p-3 border border-purple-800/30">
              <div ref={listRef} className="h-[480px] overflow-auto pr-4" style={{position: 'relative'}}>
                <div className="space-y-3">
                  {futureBirthdays.current.map((b, i) => {
                    const hasComment = comments[b.year];
                    const isEditing = editingYear === b.year;
                    const canEditThis = b.age === 17 || (canEdit && b.year === new Date().getFullYear());
                    
                    return (
                      <div key={i} className="birthday-item p-4 rounded-lg bg-[rgba(147,51,234,0.08)] border border-purple-700/30 transition-all hover:bg-[rgba(147,51,234,0.12)] hover:border-purple-600/50">
                        <div className="flex justify-between items-start mb-2">
                          <div>
                            <div className="text-sm font-bold text-purple-300">
                              {b.age} años
                              {b.age === currentAge && <Gift className="inline-block w-4 h-4 ml-2 text-yellow-400" />}
                              {b.age === 17 && <span className="ml-2 text-xs bg-purple-600 px-2 py-1 rounded-full text-white">Especial</span>}
                              {b.year === new Date().getFullYear() && canEdit && <span className="ml-2 text-xs bg-green-600 px-2 py-1 rounded-full text-white">¡Hoy!</span>}
                            </div>
                            <div className="text-xs text-slate-400 capitalize">{b.date.toLocaleDateString('es-ES', { weekday: 'long' })}</div>
                          </div>
                          <div className="flex items-center gap-3">
                            <div className="text-sm font-medium text-slate-200">{b.date.toLocaleDateString('es-ES')}</div>
                            {!hasComment && canEditThis && (
                              <button
                                onClick={() => startEdit(b.year, b.age)}
                                className="p-2 rounded-md bg-green-600/20 hover:bg-green-600/30 text-green-400 transition-all"
                                title="Agregar comentario"
                              >
                                <Plus className="w-4 h-4" />
                              </button>
                            )}
                            {hasComment && canEditThis && (
                              <button
                                onClick={() => startEdit(b.year, b.age, hasComment.comment)}
                                className="p-2 rounded-md bg-blue-600/20 hover:bg-blue-600/30 text-blue-400 transition-all"
                                title="Editar comentario"
                              >
                                <Edit3 className="w-4 h-4" />
                              </button>
                            )}
                          </div>
                        </div>

                        {/* Show existing comment */}
                        {hasComment && !isEditing && (
                          <div className="mt-2 p-3 bg-[rgba(0,0,0,0.3)] rounded-md border-l-4 border-purple-500">
                            <div className="text-sm text-slate-200">{hasComment.comment}</div>
                            <div className="text-xs text-slate-500 mt-1">
                              Guardado: {new Date(hasComment.created_at).toLocaleDateString('es-ES')}
                            </div>
                          </div>
                        )}

                        {/* Edit form */}
                        {isEditing && (
                          <div className="mt-2 p-3 bg-[rgba(0,0,0,0.4)] rounded-md border border-purple-500/50">
                            <textarea
                              value={commentText}
                              onChange={(e) => setCommentText(e.target.value)}
                              placeholder="¿Cómo estuvo el cumpleaños?"
                              className="w-full h-20 p-2 rounded-md bg-[rgba(147,51,234,0.1)] text-sm text-white resize-none outline-none border border-purple-700/30 focus:border-purple-500"
                              autoFocus
                            />
                            <div className="flex gap-2 mt-2">
                              <button
                                onClick={() => saveComment(b.year, b.age)}
                                className="flex-1 px-3 py-2 rounded-md bg-gradient-to-r from-purple-600 to-blue-700 text-white font-semibold inline-flex items-center justify-center gap-2 hover:shadow-lg transition-all"
                              >
                                <Check className="w-4 h-4" /> Guardar
                              </button>
                              <button
                                onClick={cancelEdit}
                                className="px-3 py-2 rounded-md border border-purple-700/50 text-slate-300 hover:bg-purple-800/20 transition-all"
                              >
                                Cancelar
                              </button>
                            </div>
                          </div>
                        )}
                      </div>
                    );
                  })}
                </div>
              </div>

              {/* scroll controls */}
              <div className="absolute right-6 top-[180px] flex flex-col gap-2">
                <button onClick={() => scrollList(-180)} className="w-9 h-9 rounded-md bg-purple-800/30 text-white hover:bg-purple-700/50 transition-all border border-purple-700/50">▲</button>
                <button onClick={() => scrollList(180)} className="w-9 h-9 rounded-md bg-purple-800/30 text-white hover:bg-purple-700/50 transition-all border border-purple-700/50">▼</button>
              </div>
            </div>

            {/* final message */}
            {showBirthdays && (
              <div className="bg-gradient-to-r from-purple-700 to-blue-900 text-white p-4 rounded-lg text-center animate-fade-in">
                <h3 className="text-xl font-bold">❤️ Te quiero ❤️</h3>
                <p className="text-sm mt-1">Más que a nadie en este mundo. Eres la mejor hermana que alguien podría tener.</p>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* floating hearts */}
      <div className="pointer-events-none fixed inset-0 -z-10">
        {[...Array(12)].map((_, i) => (
          <Heart key={i} className="absolute text-purple-500/8" style={{ left: `${(i * 13) % 100}%`, top: `${(i * 21) % 100}%`, width: `${20 + (i % 5) * 8}px`, transform: `translateY(${(i % 2 ? -8 : 6)}px)` }} />
        ))}
      </div>
    </div>
  );
}

export default App;