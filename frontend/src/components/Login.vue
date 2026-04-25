<template>
  <div class="login-page">
    <div class="login-container">
      <!-- Logo / Header -->
      <div class="login-header">
        <div class="logo-circle">
          <ion-icon name="people"></ion-icon>
        </div>
        <h1>Sistema Comunidad</h1>
        <p>Ingresa tus credenciales para continuar</p>
      </div>

      <!-- Tabs -->
      <div class="login-tabs">
        <button
          :class="['tab', { active: modo === 'password' }]"
          @click="modo = 'password'; resetear()"
        >
          <ion-icon name="key-outline"></ion-icon>
          Contraseña
        </button>
        <button
          :class="['tab', { active: modo === 'facial' }]"
          @click="modo = 'facial'; resetear()"
        >
          <ion-icon name="scan-outline"></ion-icon>
          Reconocimiento Facial
        </button>
      </div>

      <!-- Modo: Usuario + Contraseña -->
      <div v-if="modo === 'password'" class="login-form">
        <div class="campo">
          <label>DNI o Usuario</label>
          <div class="input-icon">
            <ion-icon name="person-outline"></ion-icon>
            <input
              v-model="credenciales.username"
              type="text"
              placeholder="Ingresa tu DNI o usuario"
              @keyup.enter="iniciarSesion"
              :disabled="cargando"
            />
          </div>
        </div>

        <div class="campo">
          <label>Contraseña</label>
          <div class="input-icon">
            <ion-icon name="lock-closed-outline"></ion-icon>
            <input
              v-model="credenciales.password"
              :type="mostrarPassword ? 'text' : 'password'"
              placeholder="Ingresa tu contraseña"
              @keyup.enter="iniciarSesion"
              :disabled="cargando"
            />
            <button class="toggle-password" @click="mostrarPassword = !mostrarPassword" type="button">
              <ion-icon :name="mostrarPassword ? 'eye-off-outline' : 'eye-outline'"></ion-icon>
            </button>
          </div>
        </div>

        <button class="btn-login" @click="iniciarSesion" :disabled="cargando || !credenciales.username || !credenciales.password">
          <ion-icon v-if="!cargando" name="log-in-outline"></ion-icon>
          <div v-else class="spinner-small"></div>
          {{ cargando ? 'Verificando...' : 'Ingresar' }}
        </button>
      </div>

      <!-- Modo: Reconocimiento Facial -->
      <div v-if="modo === 'facial'" class="login-facial">
        <div class="camara-container" :class="{ activa: camaraActiva, reconociendo: reconociendo }">
          <video ref="videoRef" autoplay playsinline muted></video>
          <canvas ref="canvasRef" style="display:none"></canvas>

          <!-- Overlay de escaneo -->
          <div class="scan-overlay" v-if="camaraActiva">
            <div class="scan-frame">
              <div class="corner tl"></div>
              <div class="corner tr"></div>
              <div class="corner bl"></div>
              <div class="corner br"></div>
            </div>
            <div class="scan-line" v-if="reconociendo"></div>
          </div>

          <!-- Placeholder cuando cámara off -->
          <div class="camara-placeholder" v-if="!camaraActiva">
            <ion-icon name="camera-outline"></ion-icon>
            <p>Cámara desactivada</p>
          </div>
        </div>

        <div class="facial-controles">
          <button v-if="!camaraActiva" class="btn-camara" @click="activarCamara">
            <ion-icon name="camera-outline"></ion-icon>
            Activar Cámara
          </button>

          <template v-else>
            <button class="btn-escanear" @click="capturarYReconocer" :disabled="reconociendo">
              <ion-icon v-if="!reconociendo" name="scan-circle-outline"></ion-icon>
              <div v-else class="spinner-small"></div>
              {{ reconociendo ? 'Reconociendo...' : 'Escanear Rostro' }}
            </button>
            <button class="btn-detener" @click="detenerCamara">
              <ion-icon name="stop-circle-outline"></ion-icon>
              Detener
            </button>
          </template>
        </div>

        <p class="facial-hint">
          <ion-icon name="information-circle-outline"></ion-icon>
          Coloca tu rostro frente a la cámara y presiona "Escanear Rostro"
        </p>
      </div>

      <!-- Mensaje de error / éxito -->
      <div v-if="mensaje" :class="['mensaje', mensaje.tipo]">
        <ion-icon :name="mensaje.tipo === 'error' ? 'alert-circle-outline' : 'checkmark-circle-outline'"></ion-icon>
        {{ mensaje.texto }}
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onUnmounted } from 'vue'
import authService from '@/services/auth.service'

const emit = defineEmits(['autenticado'])

const modo = ref<'password' | 'facial'>('password')
const cargando = ref(false)
const reconociendo = ref(false)
const mostrarPassword = ref(false)
const camaraActiva = ref(false)
const mensaje = ref<{ tipo: string; texto: string } | null>(null)

const credenciales = ref({ username: '', password: '' })
const videoRef = ref<HTMLVideoElement | null>(null)
const canvasRef = ref<HTMLCanvasElement | null>(null)
let stream: MediaStream | null = null

const resetear = () => {
  mensaje.value = null
  if (stream) detenerCamara()
}

const iniciarSesion = async () => {
  if (!credenciales.value.username || !credenciales.value.password) return
  cargando.value = true
  mensaje.value = null
  try {
    const result = await authService.login(credenciales.value.username, credenciales.value.password)
    authService.guardarSesion(result.token, result.usuario)
    mensaje.value = { tipo: 'success', texto: `Bienvenido, ${result.usuario.nombre_completo}` }
    setTimeout(() => emit('autenticado', result.usuario), 800)
  } catch (error: any) {
    mensaje.value = { tipo: 'error', texto: error.response?.data?.detail || 'Credenciales incorrectas' }
  } finally {
    cargando.value = false
  }
}

const activarCamara = async () => {
  try {
    stream = await navigator.mediaDevices.getUserMedia({ video: { facingMode: 'user', width: 640, height: 480 } })
    if (videoRef.value) {
      videoRef.value.srcObject = stream
    }
    camaraActiva.value = true
    mensaje.value = null
  } catch (error) {
    mensaje.value = { tipo: 'error', texto: 'No se pudo acceder a la cámara. Verifica los permisos.' }
  }
}

const detenerCamara = () => {
  if (stream) {
    stream.getTracks().forEach(t => t.stop())
    stream = null
  }
  camaraActiva.value = false
}

const capturarYReconocer = async () => {
  if (!videoRef.value || !canvasRef.value) return
  reconociendo.value = true
  mensaje.value = null

  try {
    const video = videoRef.value
    const canvas = canvasRef.value
    canvas.width = video.videoWidth
    canvas.height = video.videoHeight
    const ctx = canvas.getContext('2d')!
    ctx.drawImage(video, 0, 0)
    const foto_base64 = canvas.toDataURL('image/jpeg', 0.8)

    const result = await authService.loginFacial(foto_base64)
    authService.guardarSesion(result.token, result.usuario)
    mensaje.value = { tipo: 'success', texto: result.message }
    detenerCamara()
    setTimeout(() => emit('autenticado', result.usuario), 800)
  } catch (error: any) {
    mensaje.value = { tipo: 'error', texto: error.response?.data?.detail || 'Rostro no reconocido' }
  } finally {
    reconociendo.value = false
  }
}

onUnmounted(() => {
  if (stream) detenerCamara()
})
</script>

<style scoped>
.login-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #1a1f2e 0%, #2d3561 50%, #1a1f2e 100%);
}

.login-container {
  background: white;
  border-radius: 20px;
  padding: 2.5rem;
  width: 420px;
  max-width: 95vw;
  box-shadow: 0 25px 60px rgba(0,0,0,0.4);
}

.login-header {
  text-align: center;
  margin-bottom: 2rem;
}

.logo-circle {
  width: 72px;
  height: 72px;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea, #764ba2);
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 1rem;
  font-size: 2rem;
  color: white;
}

.login-header h1 {
  font-size: 1.6rem;
  color: #1a1f2e;
  margin-bottom: 0.3rem;
}

.login-header p {
  color: #7f8c8d;
  font-size: 0.9rem;
}

.login-tabs {
  display: flex;
  gap: 0;
  margin-bottom: 1.5rem;
  border-radius: 10px;
  overflow: hidden;
  border: 1px solid #e0e0e0;
}

.tab {
  flex: 1;
  padding: 0.75rem;
  border: none;
  background: #f5f5f5;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.4rem;
  font-size: 0.85rem;
  color: #666;
  transition: all 0.2s;
}

.tab.active {
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: white;
  font-weight: 600;
}

.login-form { display: flex; flex-direction: column; gap: 1.2rem; }

.campo label {
  display: block;
  font-size: 0.85rem;
  font-weight: 600;
  color: #444;
  margin-bottom: 0.4rem;
}

.input-icon {
  position: relative;
  display: flex;
  align-items: center;
}

.input-icon ion-icon:first-child {
  position: absolute;
  left: 0.9rem;
  color: #999;
  font-size: 1.1rem;
  pointer-events: none;
}

.input-icon input {
  width: 100%;
  padding: 0.75rem 1rem 0.75rem 2.7rem;
  border: 1.5px solid #ddd;
  border-radius: 10px;
  font-size: 0.95rem;
  transition: border-color 0.2s;
  box-sizing: border-box;
}

.input-icon input:focus {
  outline: none;
  border-color: #667eea;
}

.toggle-password {
  position: absolute;
  right: 0.9rem;
  background: none;
  border: none;
  cursor: pointer;
  color: #999;
  font-size: 1.1rem;
  display: flex;
}

.btn-login {
  padding: 0.85rem;
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: white;
  border: none;
  border-radius: 10px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  transition: opacity 0.2s;
  margin-top: 0.5rem;
}

.btn-login:disabled { opacity: 0.6; cursor: not-allowed; }

/* Facial */
.login-facial { display: flex; flex-direction: column; align-items: center; gap: 1rem; }

.camara-container {
  width: 100%;
  aspect-ratio: 4/3;
  border-radius: 14px;
  overflow: hidden;
  background: #1a1f2e;
  position: relative;
  border: 2px solid #ddd;
  transition: border-color 0.3s;
}

.camara-container.activa { border-color: #667eea; }
.camara-container.reconociendo { border-color: #27ae60; }

.camara-container video {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transform: scaleX(-1);
}

.camara-placeholder {
  position: absolute;
  inset: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: #555;
  gap: 0.5rem;
  font-size: 0.9rem;
}

.camara-placeholder ion-icon { font-size: 3rem; color: #667eea; }

.scan-overlay {
  position: absolute;
  inset: 0;
  display: flex;
  align-items: center;
  justify-content: center;
}

.scan-frame {
  width: 65%;
  aspect-ratio: 1;
  position: relative;
}

.corner {
  position: absolute;
  width: 20px;
  height: 20px;
  border-color: #667eea;
  border-style: solid;
}

.corner.tl { top: 0; left: 0; border-width: 3px 0 0 3px; }
.corner.tr { top: 0; right: 0; border-width: 3px 3px 0 0; }
.corner.bl { bottom: 0; left: 0; border-width: 0 0 3px 3px; }
.corner.br { bottom: 0; right: 0; border-width: 0 3px 3px 0; }

.scan-line {
  position: absolute;
  top: 20%;
  left: 10%;
  right: 10%;
  height: 2px;
  background: linear-gradient(90deg, transparent, #27ae60, transparent);
  animation: scan 1.5s ease-in-out infinite;
}

@keyframes scan {
  0% { top: 20%; }
  50% { top: 75%; }
  100% { top: 20%; }
}

.facial-controles {
  display: flex;
  gap: 0.8rem;
  width: 100%;
}

.btn-camara, .btn-escanear, .btn-detener {
  flex: 1;
  padding: 0.75rem;
  border: none;
  border-radius: 10px;
  font-size: 0.9rem;
  font-weight: 600;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.4rem;
  transition: opacity 0.2s;
}

.btn-camara { background: #667eea; color: white; }
.btn-escanear { background: #27ae60; color: white; }
.btn-detener { background: #e74c3c; color: white; flex: 0 0 auto; padding: 0.75rem 1rem; }
.btn-escanear:disabled { opacity: 0.6; cursor: not-allowed; }

.facial-hint {
  font-size: 0.8rem;
  color: #999;
  text-align: center;
  display: flex;
  align-items: center;
  gap: 0.3rem;
}

.mensaje {
  margin-top: 1rem;
  padding: 0.75rem 1rem;
  border-radius: 10px;
  font-size: 0.9rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.mensaje.error { background: #fde8e8; color: #c0392b; }
.mensaje.success { background: #e8f8f0; color: #27ae60; }

.spinner-small {
  width: 16px;
  height: 16px;
  border: 2px solid rgba(255,255,255,0.3);
  border-top-color: white;
  border-radius: 50%;
  animation: spin 0.6s linear infinite;
}

@keyframes spin { to { transform: rotate(360deg); } }

@media (max-width: 480px) {
  .login-container {
    padding: 1.5rem;
    border-radius: 0;
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    justify-content: center;
  }
  .login-page { align-items: stretch; }
  .login-header h1 { font-size: 1.3rem; }
  .logo-circle { width: 56px; height: 56px; font-size: 1.5rem; }
}
</style>
