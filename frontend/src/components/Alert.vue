<template>
  <Teleport to="body">
    <transition name="slide-fade">
      <div v-if="visible" :class="['alert-container', `alert-${type}`]">
        <div class="alert-content">
          <ion-icon :name="iconName" class="alert-icon"></ion-icon>
          <div class="alert-text">
            <p class="alert-title">{{ title }}</p>
            <p v-if="message" class="alert-message">{{ message }}</p>
          </div>
          <button class="alert-close" @click="close">
            <ion-icon name="close-outline"></ion-icon>
          </button>
        </div>
      </div>
    </transition>
  </Teleport>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  type: {
    type: String,
    default: 'info',
    validator: (v) => ['success', 'error', 'warning', 'info'].includes(v)
  },
  title: {
    type: String,
    required: true
  },
  message: {
    type: String,
    default: ''
  },
  visible: {
    type: Boolean,
    default: false
  },
  duration: {
    type: Number,
    default: 4000
  }
})

const emit = defineEmits(['close'])

const iconName = computed(() => {
  const icons = {
    success: 'checkmark-circle',
    error: 'alert-circle',
    warning: 'warning',
    info: 'information-circle'
  }
  return icons[props.type]
})

const close = () => {
  emit('close')
}

if (props.visible && props.duration > 0) {
  setTimeout(() => {
    close()
  }, props.duration)
}
</script>

<style scoped>
.alert-container {
  position: fixed;
  top: 20px;
  right: 20px;
  z-index: 9999;
  max-width: 450px;
  border-radius: 12px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
  backdrop-filter: blur(10px);
  animation: slideIn 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.alert-content {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  padding: 16px 20px;
}

.alert-icon {
  font-size: 24px;
  flex-shrink: 0;
  margin-top: 2px;
}

.alert-text {
  flex: 1;
  min-width: 0;
}

.alert-title {
  margin: 0;
  font-weight: 600;
  font-size: 15px;
  line-height: 1.4;
}

.alert-message {
  margin: 4px 0 0;
  font-size: 13px;
  opacity: 0.9;
  line-height: 1.4;
  word-break: break-word;
}

.alert-close {
  background: none;
  border: none;
  cursor: pointer;
  padding: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
  flex-shrink: 0;
  border-radius: 6px;
  transition: background 0.2s;
}

.alert-close:hover {
  background: rgba(0, 0, 0, 0.1);
}

/* Success */
.alert-success {
  background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%);
  color: #155724;
  border: 1px solid #b1dfbb;
}

.alert-success .alert-close {
  color: #155724;
}

.alert-success .alert-icon {
  color: #28a745;
}

/* Error */
.alert-error {
  background: linear-gradient(135deg, #f8d7da 0%, #f5c6cb 100%);
  color: #721c24;
  border: 1px solid #f1b0b7;
}

.alert-error .alert-close {
  color: #721c24;
}

.alert-error .alert-icon {
  color: #dc3545;
}

/* Warning */
.alert-warning {
  background: linear-gradient(135deg, #fff3cd 0%, #ffeaa7 100%);
  color: #856404;
  border: 1px solid #ffeaa7;
}

.alert-warning .alert-close {
  color: #856404;
}

.alert-warning .alert-icon {
  color: #ffc107;
}

/* Info */
.alert-info {
  background: linear-gradient(135deg, #d1ecf1 0%, #bee5eb 100%);
  color: #0c5460;
  border: 1px solid #bee5eb;
}

.alert-info .alert-close {
  color: #0c5460;
}

.alert-info .alert-icon {
  color: #17a2b8;
}

@keyframes slideIn {
  from {
    transform: translateX(400px);
    opacity: 0;
  }
  to {
    transform: translateX(0);
    opacity: 1;
  }
}

.slide-fade-enter-active {
  animation: slideIn 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.slide-fade-leave-active {
  animation: slideOut 0.3s ease-in;
}

@keyframes slideOut {
  from {
    transform: translateX(0);
    opacity: 1;
  }
  to {
    transform: translateX(400px);
    opacity: 0;
  }
}

@media (max-width: 768px) {
  .alert-container {
    left: 12px;
    right: 12px;
    max-width: none;
  }

  .alert-content {
    padding: 12px 16px;
  }

  .alert-title {
    font-size: 14px;
  }

  .alert-message {
    font-size: 12px;
  }
}
</style>
