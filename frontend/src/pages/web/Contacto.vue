<template>
  <LayoutPublico>
    <section class="page-hero" :style="{ backgroundImage: `url('/uploads/img/variadas/1.png')` }">
      <div class="ph-overlay"></div>
      <div class="ph-content">
        <span class="ph-tag"><ion-icon name="call-outline"></ion-icon> Contacto</span>
        <h1>Contáctanos</h1>
        <p>Escríbenos o visítanos para cualquier consulta sobre la comunidad o ECOSER</p>
      </div>
    </section>

    <section class="section">
      <div class="container">
        <div class="contacto-grid">
          <!-- Formulario -->
          <div class="form-box">
            <h2>Envíanos un mensaje</h2>
            <p>Responderemos a la brevedad posible a través de nuestros canales oficiales.</p>
            <form @submit.prevent="enviarFormulario" class="form">
              <div class="form-row">
                <div class="form-group">
                  <label>Nombre completo *</label>
                  <input v-model="form.nombre" type="text" placeholder="Tu nombre" required />
                </div>
                <div class="form-group">
                  <label>Correo electrónico *</label>
                  <input v-model="form.email" type="email" placeholder="tu@email.com" required />
                </div>
              </div>
              <div class="form-group">
                <label>Asunto *</label>
                <select v-model="form.asunto" required>
                  <option value="">Selecciona un asunto</option>
                  <option value="informacion">Información general sobre la comunidad</option>
                  <option value="ecoser">Servicios de ECOSER</option>
                  <option value="Usuario">Trámites de empadronamiento</option>
                  <option value="territorio">Consulta sobre territorio</option>
                  <option value="otro">Otro</option>
                </select>
              </div>
              <div class="form-group">
                <label>Mensaje *</label>
                <textarea v-model="form.mensaje" rows="5" placeholder="Escribe tu consulta aquí..." required></textarea>
              </div>
              <button type="submit" class="btn-submit" :disabled="enviando">
                <ion-icon :name="enviando ? 'hourglass-outline' : 'send-outline'"></ion-icon>
                {{ enviando ? 'Enviando...' : 'Enviar mensaje' }}
              </button>
              <div v-if="enviado" class="success-msg">
                <ion-icon name="checkmark-circle-outline"></ion-icon>
                ¡Mensaje enviado! Nos comunicaremos contigo pronto.
              </div>
            </form>
          </div>

          <!-- Info de contacto -->
          <div class="info-box">
            <div class="info-card">
              <div v-for="info in contactoInfo" :key="info.label" class="info-item">
                <div class="info-icon"><ion-icon :name="info.icon"></ion-icon></div>
                <div>
                  <strong>{{ info.label }}</strong>
                  <span>{{ info.valor }}</span>
                </div>
              </div>
            </div>

            <div class="horario-card">
              <h3><ion-icon name="time-outline"></ion-icon> Horario de atención</h3>
              <div class="horario-lista">
                <div class="h-row"><span>Lunes a Viernes</span><span>8:00 am – 1:00 pm</span></div>
                <div class="h-row"><span></span><span>3:00 pm – 6:00 pm</span></div>
                <div class="h-row"><span>Sábados</span><span>8:00 am – 12:00 pm</span></div>
                <div class="h-row"><span>Domingos</span><span>Cerrado</span></div>
              </div>
            </div>

            <div class="ecoser-contact">
              <div class="ec-header">
                <ion-icon name="briefcase-outline"></ion-icon>
                <div>
                  <strong>Empresa ECOSER</strong>
                  <span>Servicios y contrataciones</span>
                </div>
              </div>
              <p>Para servicios de alquiler de camionetas, provisión de mano de obra o apoyo logístico, comunícate directamente con ECOSER.</p>
            </div>
          </div>
        </div>
      </div>
    </section>

    <section class="section bg-light">
      <div class="container">
        <div class="ubicacion-box">
          <div class="ub-text">
            <span class="tag">Cómo llegar</span>
            <h2>Nuestra Ubicación</h2>
            <p>La sede comunal se encuentra en el distrito de Torata, provincia de Mariscal Nieto, región Moquegua. Fácilmente accesible desde la ciudad de Moquegua.</p>
            <div class="ub-datos">
              <div class="ub-dato" v-for="d in ubicacion" :key="d.label">
                <ion-icon :name="d.icon"></ion-icon>
                <div>
                  <strong>{{ d.label }}</strong>
                  <span>{{ d.valor }}</span>
                </div>
              </div>
            </div>
          </div>
          <div class="ub-map">
            <div class="map-placeholder">
              <ion-icon name="map-outline"></ion-icon>
              <p>Torata, Mariscal Nieto<br>Moquegua, Perú</p>
            </div>
          </div>
        </div>
      </div>
    </section>
  </LayoutPublico>
</template>

<script setup>
import { ref } from 'vue'
import LayoutPublico from './LayoutPublico.vue'

const enviando = ref(false)
const enviado = ref(false)

const form = ref({ nombre: '', email: '', asunto: '', mensaje: '' })

function enviarFormulario() {
  enviando.value = true
  setTimeout(() => {
    enviando.value = false
    enviado.value = true
    form.value = { nombre: '', email: '', asunto: '', mensaje: '' }
    setTimeout(() => { enviado.value = false }, 5000)
  }, 1500)
}

const contactoInfo = [
  { icon: 'location-outline', label: 'Dirección', valor: 'Torata, Mariscal Nieto, Moquegua' },
  { icon: 'call-outline', label: 'Teléfono', valor: '+51 053 462 000' },
  { icon: 'mail-outline', label: 'Correo', valor: 'comunidad@tpct.pe' },
  { icon: 'globe-outline', label: 'Región', valor: 'Moquegua, Perú' },
]

const ubicacion = [
  { icon: 'location-outline', label: 'Distrito', valor: 'Torata' },
  { icon: 'map-outline', label: 'Provincia', valor: 'Mariscal Nieto' },
  { icon: 'earth-outline', label: 'Región', valor: 'Moquegua' },
  { icon: 'navigate-outline', label: 'Referencia', valor: 'A 30 km de la ciudad de Moquegua' },
]
</script>

<style scoped>
.page-hero { min-height: 50vh; background-size: cover; background-position: center; display: flex; align-items: center; position: relative; }
.ph-overlay { position: absolute; inset: 0; background: rgba(5,20,8,0.78); }
.ph-content { position: relative; z-index: 2; max-width: 1200px; margin: 0 auto; padding: 120px 24px 80px; color: white; }
.ph-tag { display: inline-flex; align-items: center; gap: 8px; padding: 6px 16px; background: rgba(134,239,172,0.15); color: #86efac; border-radius: 100px; font-size: 13px; font-weight: 600; margin-bottom: 16px; }
.ph-content h1 { font-size: clamp(2rem,4vw,3rem); font-weight: 800; margin-bottom: 10px; }
.ph-content p { font-size: 16px; color: rgba(255,255,255,0.7); }

.section { padding: 96px 0; background: white; }
.section.bg-light { background: white; }
.container { max-width: 1200px; margin: 0 auto; padding: 0 24px; }
.tag { display: inline-block; padding: 4px 14px; background: #dcfce7; color: #15803d; border-radius: 100px; font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 12px; }

.contacto-grid { display: grid; grid-template-columns: 1fr 420px; gap: 48px; align-items: start; }

.form-box h2 { font-size: 1.8rem; font-weight: 800; color: #1a2e1a; margin-bottom: 8px; }
.form-box > p { font-size: 15px; color: #4a5e4a; margin-bottom: 32px; }
.form { display: flex; flex-direction: column; gap: 20px; }
.form-row { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }
.form-group { display: flex; flex-direction: column; gap: 6px; }
.form-group label { font-size: 13px; font-weight: 600; color: #374151; }
.form-group input, .form-group select, .form-group textarea { padding: 11px 14px; border: 1px solid #d1d5db; border-radius: 10px; font-size: 14px; color: #1e293b; background: white; outline: none; transition: border-color 0.2s; font-family: inherit; }
.form-group input:focus, .form-group select:focus, .form-group textarea:focus { border-color: #16a34a; box-shadow: 0 0 0 3px rgba(22,163,74,0.1); }
.form-group textarea { resize: vertical; }
.btn-submit { display: inline-flex; align-items: center; justify-content: center; gap: 8px; padding: 13px 28px; background: #16a34a; color: white; border: none; border-radius: 10px; font-size: 15px; font-weight: 700; cursor: pointer; transition: all 0.2s; }
.btn-submit:hover:not(:disabled) { background: #15803d; }
.btn-submit:disabled { opacity: 0.6; cursor: not-allowed; }
.success-msg { display: flex; align-items: center; gap: 10px; padding: 14px 18px; background: #f0fdf4; border: 1px solid #bbf7d0; border-radius: 10px; color: #15803d; font-size: 14px; font-weight: 600; }
.success-msg ion-icon { font-size: 20px; flex-shrink: 0; }

.info-box { display: flex; flex-direction: column; gap: 20px; }
.info-card { background: #f8fafc; border-radius: 16px; border: 1px solid #e2e8f0; padding: 24px; display: flex; flex-direction: column; gap: 20px; }
.info-item { display: flex; align-items: flex-start; gap: 14px; }
.info-icon { width: 40px; height: 40px; background: #dcfce7; border-radius: 10px; display: flex; align-items: center; justify-content: center; font-size: 20px; color: #16a34a; flex-shrink: 0; }
.info-item strong { display: block; font-size: 13px; font-weight: 700; color: #1a2e1a; margin-bottom: 2px; }
.info-item span { font-size: 14px; color: #4a5e4a; }

.horario-card { background: #f8fafc; border-radius: 16px; border: 1px solid #e2e8f0; padding: 24px; }
.horario-card h3 { display: flex; align-items: center; gap: 8px; font-size: 15px; font-weight: 700; color: #1e293b; margin-bottom: 16px; }
.horario-card ion-icon { color: #16a34a; }
.horario-lista { display: flex; flex-direction: column; gap: 8px; }
.h-row { display: flex; justify-content: space-between; font-size: 14px; padding: 6px 0; border-bottom: 1px solid #f1f5f9; }
.h-row:last-child { border-bottom: none; }
.h-row span:first-child { font-weight: 600; color: #1e293b; }
.h-row span:last-child { color: #64748b; }

.ecoser-contact { background: linear-gradient(135deg,#0a1e0c,#16a34a); border-radius: 16px; padding: 24px; color: white; }
.ec-header { display: flex; align-items: center; gap: 14px; margin-bottom: 14px; }
.ec-header ion-icon { font-size: 32px; color: #86efac; flex-shrink: 0; }
.ec-header strong { display: block; font-size: 15px; font-weight: 700; }
.ec-header span { font-size: 13px; color: rgba(255,255,255,0.7); }
.ecoser-contact p { font-size: 13px; color: rgba(255,255,255,0.8); line-height: 1.7; }

.ubicacion-box { display: grid; grid-template-columns: 1fr 1fr; gap: 64px; align-items: center; }
.ub-text { display: flex; flex-direction: column; gap: 16px; }
.ub-text h2 { font-size: 2rem; font-weight: 800; color: #1a2e1a; }
.ub-text > p { font-size: 15px; color: #4a5e4a; line-height: 1.8; }
.ub-datos { display: grid; grid-template-columns: 1fr 1fr; gap: 14px; }
.ub-dato { display: flex; align-items: center; gap: 12px; background: #f8fafc; border-radius: 10px; padding: 14px; border: 1px solid #e2e8f0; }
.ub-dato ion-icon { font-size: 22px; color: #16a34a; flex-shrink: 0; }
.ub-dato strong { display: block; font-size: 13px; font-weight: 700; color: #1a2e1a; }
.ub-dato span { font-size: 12px; color: #4a5e4a; }
.ub-map { border-radius: 20px; overflow: hidden; }
.map-placeholder { height: 400px; background: linear-gradient(135deg,#0a1e0c,#16a34a); display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 16px; color: white; border-radius: 20px; }
.map-placeholder ion-icon { font-size: 64px; color: #86efac; }
.map-placeholder p { font-size: 18px; font-weight: 600; text-align: center; line-height: 1.6; color: rgba(255,255,255,0.9); }

@media (max-width: 1024px) { .contacto-grid { grid-template-columns: 1fr; } }
@media (max-width: 768px) { .form-row { grid-template-columns: 1fr; } .ubicacion-box { grid-template-columns: 1fr; } .ub-datos { grid-template-columns: 1fr; } }
</style>
